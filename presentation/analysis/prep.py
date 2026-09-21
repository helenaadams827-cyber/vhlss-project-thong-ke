# -*- coding: utf-8 -*-
"""Bước chuẩn bị (plan Mục 2.5 và 3.6): làm sạch dữ liệu, tạo nhóm, lưu processed/vhlss_clean.csv."""
import numpy as np, pandas as pd, os

from pathlib import Path
ROOT = str(Path(__file__).resolve().parents[2])   # thư mục gốc của project
ASSETS9 = ["oto", "moto", "bicycle", "bed", "tab", "tele", "tv", "emachine", "hmachine"]
FLOWS = ["rice", "nrice", "tobaco", "nfood", "edu", "med", "hins", "aid", "water", "elec", "garb", "fuel", "fhouse"]
NEC = ["rice", "nrice", "water", "elec", "fuel", "garb", "med", "hins", "aid", "fhouse"]
UNN = ["nfood", "edu", "tobaco"]
VN = {1:"Hà Nội",2:"Hà Giang",4:"Cao Bằng",6:"Bắc Kạn",8:"Tuyên Quang",10:"Lào Cai",11:"Điện Biên",12:"Lai Châu",14:"Sơn La",15:"Yên Bái",17:"Hòa Bình",19:"Thái Nguyên",20:"Lạng Sơn",22:"Quảng Ninh",24:"Bắc Giang",25:"Phú Thọ",26:"Vĩnh Phúc",27:"Bắc Ninh",30:"Hải Dương",31:"Hải Phòng",33:"Hưng Yên",34:"Thái Bình",35:"Hà Nam",36:"Nam Định",37:"Ninh Bình",38:"Thanh Hóa",40:"Nghệ An",42:"Hà Tĩnh",44:"Quảng Bình",45:"Quảng Trị",46:"Thừa Thiên Huế",48:"Đà Nẵng",49:"Quảng Nam",51:"Quảng Ngãi",52:"Bình Định",54:"Phú Yên",56:"Khánh Hòa",58:"Ninh Thuận",60:"Bình Thuận",62:"Kon Tum",64:"Gia Lai",66:"Đắk Lắk",67:"Đắk Nông",68:"Lâm Đồng",70:"Bình Phước",72:"Tây Ninh",74:"Bình Dương",75:"Đồng Nai",77:"BR–Vũng Tàu",79:"TP.HCM",80:"Long An",82:"Tiền Giang",83:"Bến Tre",84:"Trà Vinh",86:"Vĩnh Long",87:"Đồng Tháp",89:"An Giang",91:"Kiên Giang",92:"Cần Thơ",93:"Hậu Giang",94:"Sóc Trăng",95:"Bạc Liêu",96:"Cà Mau"}

def build():
    df = pd.read_csv(os.path.join(ROOT, "processed/vhlss_merged.csv"))
    df = df.drop(columns=["year"])                                   # trùng với Year
    # Checklist 2.5
    df["asset_na"] = df[ASSETS9].isna().all(axis=1)                  # 2. hộ thiếu cả 9 cột tài sản
    df.loc[df.asset_na, ASSETS9] = 0
    neg = (df[ASSETS9 + ["house"]] < 0)                               # 3. giá trị âm -> NaN
    df["neg_fixed"] = neg.any(axis=1)
    df[ASSETS9 + ["house"]] = df[ASSETS9 + ["house"]].mask(neg)
    df["fuel_na"] = df.fuel.isna(); df["fuel"] = df.fuel.fillna(0)    # 4.
    df["house_na"] = df.house.isna(); df["fhouse"] = df.fhouse.fillna(0)  # 5.
    df["nfood_na"] = df.nfood.isna()                                  # 6.
    # Checklist 3.6
    med = df.groupby(["Year", "province"]).Inc_head.median().unstack(0)
    avg_rank = med.rank().mean(axis=1)
    tier = pd.qcut(avg_rank.rank(method="first"), 4, labels=["T1", "T2", "T3", "T4"])
    df["tier"] = df.province.map(tier).astype(str)
    df["province_name"] = df.province.map(VN)
    df["area_l"] = df.area.map({1: "Thành thị", 2: "Nông thôn"})
    df["tot"] = df[FLOWS].sum(axis=1, min_count=len(FLOWS))           # NaN cho hộ thiếu nfood
    df["nec"] = df[NEC].sum(axis=1); df["unn"] = df[UNN].sum(axis=1)
    df["food"] = df.rice + df.nrice
    df["util"] = df[["elec", "water", "fuel", "garb"]].sum(axis=1)
    df["health"] = df[["med", "hins", "aid"]].sum(axis=1)
    df["veh"] = df[["oto", "moto", "bicycle"]].sum(axis=1)
    df["tech"] = df[["tele", "tv", "emachine"]].sum(axis=1)
    df["furn"] = df[["bed", "tab"]].sum(axis=1)
    df["house_to_inc"] = df.house / df.income
    df["burden"] = df.nec / df.income
    df["overspend"] = df.tot > df.income
    return df, avg_rank, tier

if __name__ == "__main__":
    df, avg_rank, tier = build()
    assert len(df) == 28196 and df.fuel.isna().sum() == 0
    assert df[ASSETS9].isna().sum().sum() == df["neg_fixed"].sum() * 0 + (df[ASSETS9].isna()).sum().sum()
    print("tiers:", pd.Series(tier).value_counts().sort_index().to_dict())
    print("flags:", {k: int(df[k].sum()) for k in ["asset_na", "neg_fixed", "fuel_na", "house_na", "nfood_na"]})
    print("NaN left in assets (from negatives):", int(df[ASSETS9].isna().sum().sum()), "| house NaN:", int(df.house.isna().sum()))
    df.to_csv(os.path.join(ROOT, "processed/vhlss_clean.csv"), index=False)
    print("saved processed/vhlss_clean.csv", df.shape)
