"""Cập nhật kiểm tra thu–chi; chỉ ô fuel trống được thay bằng 0.

Chạy từ thư mục dự án: .venv/bin/python research_plan/update_financial_diagnostics.py
Không sửa Excel gốc và không chạy kiểm định thay đổi giữa hai năm.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent
OUTPUT_DIRECTORY = PROJECT_DIRECTORY / "research_plan"
DATA_FILE = PROJECT_DIRECTORY / "dataset" / "VHLSS_2014.xls"
EXPENSE_COLUMNS = [
    "rice", "nrice", "tobaco", "nfood", "edu", "med", "hins",
    "aid", "water", "elec", "garb", "fuel", "fhouse",
]
YEAR_PRICE_INDICES = {2010: 100.0, 2014: 143.69}
SCOPES = ["All", "Q1", "Q2", "Q3", "Q4"]


def distribution_summary(values, scope, year, variable_name):
    """JB theo Chap 9: moment dùng mẫu số n; variance ở đây chỉ để chuẩn hóa."""
    values = values.dropna().to_numpy(dtype=float)
    sample_size = len(values)
    centered_values = values - values.mean()
    second_moment = np.mean(centered_values ** 2)
    skewness = np.mean(centered_values ** 3) / second_moment ** 1.5
    excess_kurtosis = np.mean(centered_values ** 4) / second_moment ** 2 - 3
    jarque_bera = sample_size * (skewness ** 2 / 6 + excess_kurtosis ** 2 / 24)
    np.testing.assert_allclose(jarque_bera, stats.jarque_bera(values).statistic)
    return {
        "scope": scope, "year": year, "variable": variable_name, "n": sample_size,
        "skewness": skewness, "excess_kurtosis": excess_kurtosis,
        "jarque_bera": jarque_bera,
        "jb_asymptotic_log10_p": -jarque_bera / (2 * np.log(10)),
        "largest_observation_SS_percent":
            100 * np.max(centered_values ** 2) / np.sum(centered_values ** 2),
        "median": np.median(values), "min": values.min(), "max": values.max(),
    }


def main():
    distribution_rows = []
    count_rows = []
    sample_audit_rows = []

    for year, price_index in YEAR_PRICE_INDICES.items():
        households = pd.read_excel(DATA_FILE, sheet_name=str(year))
        missing_fuel = households["fuel"].isna()
        # Chỉ điền fuel theo quy ước người dùng; các khoản trống khác vẫn thiếu.
        households["fuel"] = households["fuel"].fillna(0)
        valid_expenses = (
            households[EXPENSE_COLUMNS].notna().all(axis=1)
            & households[EXPENSE_COLUMNS].ge(0).all(axis=1)
        )
        valid_records = (
            valid_expenses & households["income"].ge(0)
            & households["size"].gt(0)
        )
        valid_households = households.loc[valid_records].copy()
        valid_households["total_expenses"] = valid_households[EXPENSE_COLUMNS].sum(axis=1)
        income_expense_balance = (
            valid_households["income"] - valid_households["total_expenses"]
        )
        valid_households["real_balance_million_per_person"] = (
            income_expense_balance / valid_households["size"] * 100 / price_index / 1000
        )
        valid_households["relative_income_margin"] = (
            income_expense_balance / valid_households["income"].where(
                valid_households["income"].gt(0)
            )
        )
        valid_households["expenses_exceed_income"] = (
            valid_households["total_expenses"] > valid_households["income"]
        )

        for scope in SCOPES:
            original_group = (
                pd.Series(True, index=households.index) if scope == "All"
                else households["Quart"].eq(int(scope[1:]))
            )
            group = valid_households.loc[original_group.loc[valid_households.index]]
            sample_size = len(group)
            exceed_count = int(group["expenses_exceed_income"].sum())
            count_rows.append({
                "scope": scope, "year": year, "n": sample_size,
                "expenses_exceed_income": exceed_count,
                "income_covers_expenses": sample_size - exceed_count,
            })
            sample_audit_rows.append({
                "scope": scope, "year": year,
                "original_households": int(original_group.sum()),
                "fuel_blanks_filled": int((original_group & missing_fuel).sum()),
                "valid_households": sample_size,
                "excluded_other_missing_or_invalid": int(original_group.sum()) - sample_size,
                "fuel_observed_valid_households": int(
                    (original_group & valid_records & ~missing_fuel).sum()
                ),
                "fuel_observed_expenses_exceed_income": int(
                    group.loc[~missing_fuel.loc[group.index], "expenses_exceed_income"].sum()
                ),
            })
            for variable_name in ["real_balance_million_per_person", "relative_income_margin"]:
                distribution_rows.append(
                    distribution_summary(group[variable_name], scope, year, variable_name)
                )

    counts = pd.DataFrame(count_rows)
    conditions = []
    for scope in SCOPES:
        group_counts = counts.loc[counts["scope"].eq(scope)]
        pooled_proportion = group_counts["expenses_exceed_income"].sum() / group_counts["n"].sum()
        observed_counts = group_counts[["expenses_exceed_income", "income_covers_expenses"]]
        expected_counts = np.column_stack([
            group_counts["n"] * pooled_proportion,
            group_counts["n"] * (1 - pooled_proportion),
        ])
        minimum_observed = int(observed_counts.to_numpy().min())
        minimum_expected = float(expected_counts.min())
        conditions.append({
            "scope": scope, "min_observed_count": minimum_observed,
            "min_pooled_expected_count": minimum_expected,
            "count_condition_at_least_10": minimum_observed >= 10 and minimum_expected >= 10,
        })

    pd.DataFrame(distribution_rows).to_csv(
        OUTPUT_DIRECTORY / "distribution_diagnostics_financial.csv", index=False
    )
    counts.to_csv(OUTPUT_DIRECTORY / "financial_indicator_counts.csv", index=False)
    pd.DataFrame(conditions).to_csv(
        OUTPUT_DIRECTORY / "financial_proportion_conditions.csv", index=False
    )
    pd.DataFrame(sample_audit_rows).to_csv(
        OUTPUT_DIRECTORY / "financial_sample_audit.csv", index=False
    )
    print(counts.to_string(index=False))
    print(pd.DataFrame(conditions).to_string(index=False))


if __name__ == "__main__":
    main()
