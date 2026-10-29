# -*- coding: utf-8 -*-
"""Sinh toàn bộ bảng số của báo cáo chi tiết -> presentation/tables/*.tex và numbersR.json
   Chạy: /home/trang/STATS/.venv/bin/python analysis/report_tables.py"""
import json, numpy as np, pandas as pd
from pathlib import Path
from style import ROOT, vn

OUT = Path(ROOT) / "presentation" / "tables"; OUT.mkdir(exist_ok=True)
df = pd.read_csv(f"{ROOT}/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy()
d["ov"] = d.tot > d.income
d["pc"] = d.tot / d["size"]
Y = [2010, 2012, 2014]; QS = [1, 2, 3, 4]; TS = ["T1", "T2", "T3", "T4"]
M = 1000.0
N = {}

ITEMS = [("rice", "Gạo"), ("nrice", "Thực phẩm khác"), ("nfood", "Chi ngoài ăn uống"), ("edu", "Giáo dục"),
         ("med", "Thuốc, viện phí"), ("hins", "Bảo hiểm y tế"), ("aid", "Chi hỗ trợ khám chữa bệnh"),
         ("elec", "Điện"), ("water", "Nước"), ("garb", "Rác"), ("fuel", "Nhiên liệu"),
         ("fhouse", "Sửa chữa, xây nhà"), ("tobaco", "Thuốc lá")]

def write(name, body):
    (OUT / f"{name}.tex").write_text(body, encoding="utf-8")
    print("  tables/" + name + ".tex")

def tab(cols, header, rows, note=None, spec=None):
    """cols: chuỗi định dạng cột; header: list[str]; rows: list[list[str]]"""
    s = "\\begin{tabular}{" + cols + "}\n\\toprule\n"
    s += " & ".join(header) + " \\\\\n\\midrule\n"
    for r in rows:
        s += " & ".join(r) + " \\\\\n"
    s += "\\bottomrule\n\\end{tabular}\n"
    return s

def p(x, dgt=1): return vn(x, dgt)
def pc(x, dgt=1): return vn(x, dgt) + "\\%"

# ---------------------------------------------------------------- 2. DỮ LIỆU
# T2 — cỡ mẫu
rows = []
for y in Y:
    g = df[df.Year == y]
    rows.append([str(y), vn(len(g)), vn((g.area == 1).sum()), pc((g.area == 1).mean()*100),
                 vn((g.area == 2).sum()), pc((g.area == 2).mean()*100), vn(g.province.nunique()),
                 p(g["size"].mean(), 2)])
rows.append(["\\textbf{Cộng}", "\\textbf{" + vn(len(df)) + "}", "\\textbf{" + vn((df.area == 1).sum()) + "}",
             "\\textbf{" + pc((df.area == 1).mean()*100) + "}", "\\textbf{" + vn((df.area == 2).sum()) + "}",
             "\\textbf{" + pc((df.area == 2).mean()*100) + "}", "\\textbf{63}", "\\textbf{" + p(df["size"].mean(), 2) + "}"])
write("t_sample", tab("lrrrrrrr", ["Năm", "Số hộ", "Thành thị", "\\%", "Nông thôn", "\\%", "Số tỉnh", "Số người/hộ (mean)"], rows))
N["n_total"] = int(len(df))

# T3 — làm sạch
flags = [("asset_na", "Thiếu giá trị tài sản (đặt về 0 khi hộ khai không có)"),
         ("neg_fixed", "Giá trị âm do nhập liệu (đưa về 0)"),
         ("fuel_na", "Thiếu chi nhiên liệu"),
         ("house_na", "Thiếu giá trị nhà ở"),
         ("nfood_na", "Thiếu chi ngoài ăn uống")]
rows = []
for c, lab in flags:
    if c in df.columns:
        rows.append([lab] + [vn(int(df[(df.Year == y)][c].sum())) for y in Y] + [vn(int(df[c].sum())), pc(df[c].mean()*100, 2)])
write("t_clean", tab("lrrrrr", ["Vấn đề đã xử lý", "2010", "2012", "2014", "Tổng", "\\% mẫu"], rows))

# T3b — độ nhạy của cách xử lý giá trị thiếu ở chi nhiên liệu (năm 2014)
g14f = d[d.Year == 2014].copy()
base = g14f.copy()                                   # cách đang dùng: điền 0
drop = g14f[~g14f.fuel_na].copy()                    # bỏ hẳn các hộ thiếu
imp = g14f.copy()                                    # điền median theo nhóm Q x khu vực
med_fuel = drop.groupby(["Quart", "area"]).fuel.median()
add = imp[imp.fuel_na].set_index(["Quart", "area"]).index.map(med_fuel).to_numpy()
imp.loc[imp.fuel_na, "fuel"] = add
imp["tot"] = imp.tot + (imp.fuel - base.fuel); imp["nec"] = imp.nec + (imp.fuel - base.fuel)
imp["ov"] = imp.tot > imp.income
def fuel_row(lab, fn):
    return [lab] + [fn(z) for z in (base, drop, imp)]
rows = [
    fuel_row("Số hộ năm 2014 dùng để tính", lambda z: vn(len(z))),
    fuel_row("\\% hộ Q1 chi vượt thu", lambda z: pc(z[z.Quart == 1].ov.mean()*100, 1)),
    fuel_row("Tổng chi / thu nhập của hộ Q1 (median)", lambda z: pc((z[z.Quart == 1].tot/z[z.Quart == 1].income).median()*100, 0)),
    fuel_row("Chi thiết yếu / thu nhập của hộ Q1 (median)", lambda z: pc((z[z.Quart == 1].nec/z[z.Quart == 1].income).median()*100, 0)),
    fuel_row("Chi/người toàn mẫu (median, triệu)", lambda z: p((z.tot/z["size"]).median()/M, 1)),
    fuel_row("Tỷ trọng chi nhiên liệu", lambda z: pc(z.fuel.sum()/z.tot.sum()*100, 1)),
    fuel_row("\\% hộ Q1 vượt thu ở nhóm tỉnh T1", lambda z: pc(z[(z.Quart == 1) & (z.tier == "T1")].ov.mean()*100, 0)),
    fuel_row("\\% hộ Q1 vượt thu ở nhóm tỉnh T4", lambda z: pc(z[(z.Quart == 1) & (z.tier == "T4")].ov.mean()*100, 0)),
]
write("t_fuel", tab("lrrr", ["Chỉ tiêu (năm 2014)", "Điền 0 (cách dùng trong báo cáo)",
                             "Bỏ 813 hộ thiếu", "Điền median theo Q $\\times$ khu vực"], rows))
N["fuel_na_2014"] = int(g14f.fuel_na.sum())
N["fuel_sens"] = dict(ov_q1=[round(z[z.Quart == 1].ov.mean()*100, 1) for z in (base, drop, imp)],
                      share=[round(z.fuel.sum()/z.tot.sum()*100, 1) for z in (base, drop, imp)])

# ---------------------------------------------------------------- 3. MEAN vs MEDIAN
def desc(x):
    x = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(x, [25, 75])
    return dict(n=len(x), mean=x.mean(), median=np.median(x), sd=x.std(ddof=1), cv=x.std(ddof=1)/x.mean()*100,
                skew=pd.Series(x).skew(), iqr=q3 - q1, p5=np.percentile(x, 5), p95=np.percentile(x, 95),
                mn=x.min(), mx=x.max(), below=(x < x.mean()).mean()*100)
g14 = df[df.Year == 2014]
rows = []
for q in QS + ["all"]:
    z = g14 if q == "all" else g14[g14.Quart == q]
    s = desc(z.Inc_head / M)
    rows.append([("Toàn mẫu" if q == "all" else f"Q{q}"), vn(s["n"]), p(s["mean"], 2), p(s["median"], 2),
                 p(s["sd"], 2), p(s["cv"], 1), p(s["skew"], 2), p(s["iqr"], 2), p(s["p5"], 2), p(s["p95"], 2),
                 p(s["mx"], 1), pc(s["below"], 1)])
write("t_dist_q", tab("lrrrrrrrrrrr",
      ["Nhóm", "n", "Mean", "Median", "SD", "CV (\\%)", "Skew", "IQR", "P5", "P95", "Max", "\\% hộ dưới mean"], rows))
N["dist14"] = {(f"Q{q}" if q != "all" else "all"): {k: round(v, 3) for k, v in desc((g14 if q == "all" else g14[g14.Quart == q]).Inc_head / M).items()} for q in QS + ["all"]}

# T4b — mean/median theo Q qua 3 năm
rows = []
for q in QS:
    r = [f"Q{q}"]
    for y in Y:
        z = df[(df.Year == y) & (df.Quart == q)].Inc_head / M
        r += [p(z.mean(), 2), p(z.median(), 2), p(z.mean()/z.median(), 3)]
    rows.append(r)
write("t_meanmed_year", tab("l" + "rrr"*3,
      ["Nhóm"] + sum([[f"Mean {y}", f"Median {y}", "Tỷ số"] for y in Y], []), rows))

# T4c — ảnh hưởng của thước đo
rows = []
for y in Y:
    z = df[df.Year == y]
    mq = [z[z.Quart == q].Inc_head.median() for q in QS]; aq = [z[z.Quart == q].Inc_head.mean() for q in QS]
    trim = z[z.Quart == 4].Inc_head
    trim = trim[trim <= trim.quantile(0.99)].mean()
    rows.append([str(y), p(mq[3]/mq[0], 2), p(aq[3]/aq[0], 2), p(aq[3]/M, 1), p(trim/M, 1), p(mq[3]/M, 1)])
write("t_ratio_measure", tab("lrrrrr",
      ["Năm", "Q4/Q1 theo median", "Q4/Q1 theo mean", "Mean Q4 (tr)", "Mean Q4 cắt 1\\% trên (tr)", "Median Q4 (tr)"], rows))

# ---------------------------------------------------------------- 4. THU NHẬP
# T5 — median theo Q, 3 năm + tăng trưởng
rows = []
for q in QS:
    v = [df[(df.Year == y) & (df.Quart == q)].Inc_head.median()/M for y in Y]
    rows.append([f"Q{q}", p(v[0], 2), p(v[1], 2), p(v[2], 2), pc((v[1]/v[0]-1)*100, 0), pc((v[2]/v[1]-1)*100, 0), pc((v[2]/v[0]-1)*100, 0)])
v = [df[df.Year == y].Inc_head.median()/M for y in Y]
rows.append(["\\textbf{Toàn mẫu}"] + ["\\textbf{" + p(x, 2) + "}" for x in v] +
            ["\\textbf{" + pc((v[1]/v[0]-1)*100, 0) + "}", "\\textbf{" + pc((v[2]/v[1]-1)*100, 0) + "}", "\\textbf{" + pc((v[2]/v[0]-1)*100, 0) + "}"])
write("t_inc_q", tab("lrrrrrr", ["Nhóm", "2010", "2012", "2014", "2010–12", "2012–14", "2010–14"], rows))

# T6 — khoảng cách tuyệt đối/tương đối
rows = []
for y in Y:
    z = df[df.Year == y]
    m = [z[z.Quart == q].Inc_head.median()/M for q in QS]
    rows.append([str(y), p(m[0], 2), p(m[3], 2), p(m[3]-m[0], 2), p(m[3]/m[0], 2), p(m[2]-m[1], 2)])
write("t_gap", tab("lrrrrr", ["Năm", "Median Q1", "Median Q4", "Hiệu Q4−Q1", "Tỷ số Q4/Q1", "Hiệu Q3−Q2"], rows))

# T7 — cơ cấu: % hộ, % dân số, % thu nhập
rows = []
for q in QS:
    r = [f"Q{q}"]
    for y in Y:
        z = df[df.Year == y]; zq = z[z.Quart == q]
        r += [pc(zq["size"].sum()/z["size"].sum()*100, 1), pc(zq.income.sum()/z.income.sum()*100, 1)]
    rows.append(r)
write("t_share_inc", tab("l" + "rr"*3, ["Nhóm (mỗi nhóm 25\\% số hộ)"] + sum([[f"\\% dân số {y}", f"\\% thu nhập {y}"] for y in Y], []), rows))
N["share_inc"] = {f"Q{q}": [round(df[(df.Year == y) & (df.Quart == q)].income.sum()/df[df.Year == y].income.sum()*100, 1) for y in Y] for q in QS}
N["share_pop"] = {f"Q{q}": [round(df[(df.Year == y) & (df.Quart == q)]["size"].sum()/df[df.Year == y]["size"].sum()*100, 1) for y in Y] for q in QS}

# T8 — thập phân vị
rows = []
for y in [2010, 2014]:
    z = df[df.Year == y].copy()
    z["dec"] = pd.qcut(z.Inc_head.rank(method="first"), 10, labels=False) + 1
    sh = z.groupby("dec").income.sum()/z.income.sum()*100
    rows.append([str(y)] + [p(sh.loc[i], 1) for i in range(1, 11)] + [p(sh.loc[9:10].sum()/sh.loc[1:4].sum(), 2)])
write("t_decile", tab("l" + "r"*11, ["Năm"] + [f"D{i}" for i in range(1, 11)] + ["D9+D10 / D1..D4"], rows))
z = df[df.Year == 2014].copy(); z["dec"] = pd.qcut(z.Inc_head.rank(method="first"), 10, labels=False) + 1
sh = z.groupby("dec").income.sum()/z.income.sum()*100
N["dec14"] = dict(bottom40=round(sh.loc[1:4].sum(), 1), top10=round(sh.loc[10], 1), top20=round(sh.loc[9:10].sum(), 1))

# T9 — khu vực và nhóm tỉnh
rows = []
tier_lab = ["T1 (tỉnh nghèo nhất)", "T2", "T3", "T4 (tỉnh giàu nhất)"]
for lab, mask in [("Thành thị", df.area == 1), ("Nông thôn", df.area == 2)] + [(lb, df.tier == t) for t, lb in zip(TS, tier_lab)]:
    v = [df[mask & (df.Year == y)].Inc_head.median()/M for y in Y]
    n = int((mask & (df.Year == 2014)).sum())
    rows.append([lab, vn(n), p(v[0], 2), p(v[1], 2), p(v[2], 2), pc((v[2]/v[0]-1)*100, 0)])
write("t_area_tier", tab("lrrrrr", ["Nhóm", "n (2014)", "2010", "2012", "2014", "Tăng 2010–14"], rows))

# T10 — độ phân tán trong từng nhóm Q
rows = []
for q in QS:
    r = [f"Q{q}"]
    for y in Y:
        z = df[(df.Year == y) & (df.Quart == q)].Inc_head/M
        r += [p(z.std(ddof=1), 2), p(z.std(ddof=1)/z.mean()*100, 1)]
    rows.append(r)
z = df.groupby("Year").Inc_head
rows.append(["\\textbf{Toàn mẫu}"] + sum([["\\textbf{" + p(df[df.Year == y].Inc_head.std(ddof=1)/M, 2) + "}",
    "\\textbf{" + p(df[df.Year == y].Inc_head.std(ddof=1)/df[df.Year == y].Inc_head.mean()*100, 1) + "}"] for y in Y], []))
write("t_spread", tab("l" + "rr"*3, ["Nhóm"] + sum([[f"SD {y}", f"CV {y} (\\%)"] for y in Y], []), rows))
print("phần 2-4 xong")

# ---------------------------------------------------------------- 5. CHI TIÊU
g14d = d[d.Year == 2014]
rows = []
for k, lab in ITEMS:
    sh = [d[(d.Year == 2014) & (d.Quart == q)][k].sum()/d[(d.Year == 2014) & (d.Quart == q)].tot.sum()*100 for q in QS]
    z = g14d[g14d[k] > 0]
    r = np.corrcoef(np.log(z[k]/z["size"]), np.log(z.Inc_head))[0, 1]
    rows.append([lab] + [p(x, 1) for x in sh] + [p(sh[3]-sh[0], 1), pc((g14d[k] > 0).mean()*100, 0), p(r, 2)])
tot = [d[(d.Year == 2014) & (d.Quart == q)].tot.sum()/1e6 for q in QS]
write("t_spend_share", tab("lrrrrrrr", ["Khoản chi", "Q1", "Q2", "Q3", "Q4", "Q4−Q1", "\\% hộ có chi", "r với thu nhập"], rows))
N["r_items"] = {lab: round(np.corrcoef(np.log(g14d[g14d[k] > 0][k]/g14d[g14d[k] > 0]["size"]), np.log(g14d[g14d[k] > 0].Inc_head))[0, 1], 2) for k, lab in ITEMS}

# chi tiêu bình quân đầu người theo Q, 3 năm
rows = []
for q in QS:
    r = [f"Q{q}"]
    for y in Y:
        z = d[(d.Year == y) & (d.Quart == q)]
        r += [p((z.tot/z["size"]).median()/M, 1), p(z.tot.median()/M, 1)]
    rows.append(r)
write("t_spend_level", tab("l" + "rr"*3, ["Nhóm"] + sum([[f"Chi/người {y}", f"Chi/hộ {y}"] for y in Y], []), rows))

# gánh nặng
rows = []
for y in Y:
    for q in QS:
        z = d[(d.Year == y) & (d.Quart == q)]
        rows.append([str(y) if q == 1 else "", f"Q{q}",
                     pc((z.nec/z.income).median()*100, 0), pc((z.unn/z.income).median()*100, 0),
                     pc((z.tot/z.income).median()*100, 0), pc((z.food/z.tot).median()*100, 0),
                     pc((z.nec/z.tot).median()*100, 0)])
write("t_burden", tab("llrrrrr", ["Năm", "Nhóm", "Thiết yếu/thu nhập", "Chưa thiết yếu/thu nhập",
                                  "Tổng chi/thu nhập", "Thực phẩm/tổng chi", "Thiết yếu/tổng chi"], rows))
N["burden"] = {str(y): {f"Q{q}": [round((d[(d.Year == y) & (d.Quart == q)].nec/d[(d.Year == y) & (d.Quart == q)].income).median()*100),
                                   round((d[(d.Year == y) & (d.Quart == q)].tot/d[(d.Year == y) & (d.Quart == q)].income).median()*100)] for q in QS} for y in Y}

# chi vượt thu
rows = []
for y in Y:
    for q in QS:
        z = d[(d.Year == y) & (d.Quart == q)]; o = z[z.ov]; nn = z[~z.ov]
        rows.append([str(y) if q == 1 else "", f"Q{q}", vn(len(z)), pc(z.ov.mean()*100, 1),
                     pc(((o.tot-o.income)/o.income).median()*100, 0), p((o.tot-o.income).median()/M, 1),
                     pc(((nn.income-nn.tot)/nn.income).median()*100, 0), p((nn.income-nn.tot).median()/M, 1)])
write("t_overspend", tab("llrrrrrr", ["Năm", "Nhóm", "n", "\\% hộ chi vượt thu", "Thiếu hụt (\\% thu nhập)",
                                      "Thiếu hụt (triệu/hộ)", "Phần dư (\\% thu nhập)", "Phần dư (triệu/hộ)"], rows))

# chi vượt thu theo nơi ở
rows = []
for lab, mask in [("Thành thị", d.area == 1), ("Nông thôn", d.area == 2)] + [(t, d.tier == t) for t in TS]:
    r = [lab]
    for y in Y:
        z = d[mask & (d.Year == y)]
        r += [pc(z.ov.mean()*100, 0), pc(z[z.Quart == 1].ov.mean()*100, 0)]
    r += [p((d[mask & (d.Year == 2014)].tot/d[mask & (d.Year == 2014)]["size"]).median()/M, 1)]
    rows.append(r)
write("t_over_where", tab("l" + "rr"*3 + "r", ["Nơi ở"] + sum([[f"Chung {y}", f"Riêng Q1 {y}"] for y in Y], []) + ["Chi/người 2014 (tr)"], rows))
N["ov_tier_q1"] = {t: [round(d[(d.tier == t) & (d.Year == y) & (d.Quart == 1)].ov.mean()*100) for y in Y] for t in TS}

# hộ vượt thu khác hộ cân đối
rows = [["Số người trong hộ (mean)"] + sum([[p(d[(d.Quart == q) & d.ov]["size"].mean(), 2), p(d[(d.Quart == q) & ~d.ov]["size"].mean(), 2)] for q in QS], []),
        ["Chi/người (median, triệu)"] + sum([[p((d[(d.Quart == q) & d.ov].pc).median()/M, 1), p((d[(d.Quart == q) & ~d.ov].pc).median()/M, 1)] for q in QS], []),
        ["Thu nhập/người (median, triệu)"] + sum([[p(d[(d.Quart == q) & d.ov].Inc_head.median()/M, 1), p(d[(d.Quart == q) & ~d.ov].Inc_head.median()/M, 1)] for q in QS], []),
        ["Chi y tế / thu nhập (median)"] + sum([[pc((d[(d.Quart == q) & d.ov].med/d[(d.Quart == q) & d.ov].income).median()*100, 1), pc((d[(d.Quart == q) & ~d.ov].med/d[(d.Quart == q) & ~d.ov].income).median()*100, 1)] for q in QS], []),
        ["Chi giáo dục / thu nhập (median)"] + sum([[pc((d[(d.Quart == q) & d.ov].edu/d[(d.Quart == q) & d.ov].income).median()*100, 1), pc((d[(d.Quart == q) & ~d.ov].edu/d[(d.Quart == q) & ~d.ov].income).median()*100, 1)] for q in QS], [])]
write("t_behavior", tab("l" + "rr"*4, ["Chỉ tiêu"] + sum([[f"Q{q} vượt", f"Q{q} cân đối"] for q in QS], []), rows))

# cơ cấu chi: hộ vượt vs không vượt (gộp) — dùng cho hình, kèm cảnh báo gộp nhóm
rows = []
ov, no = d[d.ov], d[~d.ov]
for k, lab in ITEMS:
    a_ = ov[k].sum()/ov.tot.sum()*100; b_ = no[k].sum()/no.tot.sum()*100
    rows.append([lab, p(a_, 1), p(b_, 1), ("+" if a_ >= b_ else "") + p(a_-b_, 1)])
write("t_behavior_share", tab("lrrr", ["Khoản chi", "Hộ chi vượt thu (\\%)", "Hộ cân đối (\\%)", "Chênh (điểm \\%)"], rows))

# chênh lệch tỷ trọng tính RIÊNG trong từng nhóm Q (tránh nghịch lý gộp nhóm)
rows = []
for k, lab in ITEMS:
    r = [lab]
    for q in QS:
        a_ = d[(d.Quart == q) & d.ov][k].sum()/d[(d.Quart == q) & d.ov].tot.sum()*100
        b_ = d[(d.Quart == q) & ~d.ov][k].sum()/d[(d.Quart == q) & ~d.ov].tot.sum()*100
        r.append(("+" if a_ >= b_ else "") + p(a_-b_, 1))
    a_ = ov[k].sum()/ov.tot.sum()*100; b_ = no[k].sum()/no.tot.sum()*100
    r.append(("+" if a_ >= b_ else "") + p(a_-b_, 1))
    rows.append(r)
write("t_behavior_q", tab("lrrrrr", ["Khoản chi", "Q1", "Q2", "Q3", "Q4", "Gộp cả bốn nhóm"], rows))

# số tiền: chi bình quân đầu người của hộ vượt thu gấp mấy lần hộ cân đối, trong cùng nhóm Q
rows = []
for k, lab in ITEMS + [("tot", "\\textbf{Tổng chi}")]:
    r = [lab]
    for q in QS:
        za = d[(d.Quart == q) & d.ov]; zb = d[(d.Quart == q) & ~d.ov]
        ma = za[k].sum()/za["size"].sum(); mb = zb[k].sum()/zb["size"].sum()
        r.append(p(ma/mb, 2) if mb > 0 else "—")
    za, zb = d[d.ov], d[~d.ov]
    r.append(p((za[k].sum()/za["size"].sum())/(zb[k].sum()/zb["size"].sum()), 2))
    rows.append(r)
write("t_behavior_money", tab("lrrrrr", ["Khoản chi", "Q1", "Q2", "Q3", "Q4", "Gộp cả bốn nhóm"], rows))

# ba đơn vị đo — tất cả đều tính trên tổng của nhóm để so sánh được với nhau
rows = []
z10, z14 = d[d.Year == 2010], d[d.Year == 2014]
for k, lab in ITEMS:
    a10 = z10[k].sum()/z10["size"].sum()/M; a14 = z14[k].sum()/z14["size"].sum()/M
    s10 = z10[k].sum()/z10.tot.sum()*100;   s14 = z14[k].sum()/z14.tot.sum()*100
    i10 = z10[k].sum()/z10.income.sum()*100; i14 = z14[k].sum()/z14.income.sum()*100
    rows.append([lab, p(a10, 2), p(a14, 2), ("+" if a14 >= a10 else "") + pc((a14/a10-1)*100, 0),
                 p(s10, 1), p(s14, 1), ("+" if s14 >= s10 else "") + p(s14-s10, 1),
                 p(i10, 1), p(i14, 1)])
tt10 = z10.tot.sum()/z10["size"].sum()/M; tt14 = z14.tot.sum()/z14["size"].sum()/M
rows.append(["\\textbf{Tổng chi}", "\\textbf{" + p(tt10, 2) + "}", "\\textbf{" + p(tt14, 2) + "}",
             "\\textbf{+" + pc((tt14/tt10-1)*100, 0) + "}", "\\textbf{100,0}", "\\textbf{100,0}", "—",
             "\\textbf{" + p(z10.tot.sum()/z10.income.sum()*100, 1) + "}", "\\textbf{" + p(z14.tot.sum()/z14.income.sum()*100, 1) + "}"])
write("t_units", tab("lrrrrrrrr", ["Khoản chi", "Bình quân đồng/người 2010", "2014", "Tăng",
                                   "Tỷ trọng 2010 (\\%)", "2014 (\\%)", "Chênh (điểm \\%)",
                                   "\\% thu nhập 2010", "2014"], rows))

# ---------------------------------------------------------------- 6. TÀI SẢN
h = df[df.house.notna() & (df.house > 0)].copy()
p14 = h[h.Year == 2014].groupby("province_name").house.median()/M
n14 = h[h.Year == 2014].groupby("province_name").house.size()
p10 = h[h.Year == 2010].groupby("province_name").house.median()/M
keep = n14[n14 >= 60].index
hi = p14[keep].sort_values(ascending=False).head(10); lo = p14[keep].sort_values().head(10)
rows = []
for (a_, b_) in zip(hi.items(), lo.items()):
    rows.append([a_[0], p(a_[1], 0), vn(int(n14[a_[0]])), b_[0], p(b_[1], 0), vn(int(n14[b_[0]]))])
write("t_house_prov", tab("lrrlrr", ["Tỉnh đắt nhất", "Median (triệu)", "n", "Tỉnh rẻ nhất", "Median (triệu)", "n"], rows))
N["house_ratio"] = round(hi.iloc[0]/lo.iloc[0], 1)

rows = []
for lab, mask in [("Cả nước", h.house > 0), ("Thành thị", h.area == 1), ("Nông thôn", h.area == 2)] + [(t, h.tier == t) for t in TS]:
    v = [h[mask & (h.Year == y)].house.median()/M for y in Y]
    yr = [(h[mask & (h.Year == y)].house/h[mask & (h.Year == y)].income).median() for y in Y]
    rows.append([lab, p(v[0], 0), p(v[1], 0), p(v[2], 0), pc((v[2]/v[0]-1)*100, 0), p(yr[0], 1), p(yr[2], 1)])
write("t_house_area", tab("lrrrrrr", ["Nhóm", "2010", "2012", "2014", "Tăng 2010–14",
                                      "Số năm thu nhập 2010", "Số năm thu nhập 2014"], rows))

t = df[df.Year == 2014]
ASSETS = [("house", "Nhà ở"), ("oto", "Ô tô"), ("moto", "Xe máy"), ("bicycle", "Xe đạp"), ("tele", "Điện thoại"),
          ("tv", "TV"), ("emachine", "Máy giải trí"), ("hmachine", "Máy gia dụng")]
rows = []
for k, lab in ASSETS:
    own = [(t[t.Quart == q][k] > 0).mean()*100 for q in QS]
    med = [t[(t.Quart == q) & (t[k] > 0)][k].median()/M for q in QS]
    rows.append([lab] + [pc(x, 0) for x in own] + [p(own[3]-own[0], 0)] +
                [pc((t[t.area == 1][k] > 0).mean()*100, 0), pc((t[t.area == 2][k] > 0).mean()*100, 0),
                 p(med[0], 1), p(med[3], 1)])
write("t_assets_own", tab("lrrrrrrrrr", ["Tài sản", "Q1", "Q2", "Q3", "Q4", "Q4−Q1 (điểm)", "Thành thị", "Nông thôn",
                                          "Giá trị median Q1", "Giá trị median Q4"], rows))

rows = []
for k, lab in [("house", "Nhà ở"), ("tech", "Đồ công nghệ"), ("furn", "Nội thất"), ("veh", "Phương tiện")]:
    z = t[(t[k] > 0) & t.Inc_head.notna()]
    r_raw = np.corrcoef(z[k], z.Inc_head)[0, 1]
    r_log = np.corrcoef(np.log(z[k]), np.log(z.Inc_head))[0, 1]
    med = [t[t.Quart == q][k].median()/M for q in QS]
    rows.append([lab, vn(len(z)), p(r_raw, 2), p(r_log, 2), p(med[0], 2), p(med[3], 2), p(med[3]/max(med[0], 0.01), 1)])
write("t_assets_r", tab("lrrrrrr", ["Nhóm tài sản", "n (hộ có)", "r trên số gốc", "r trên thang log",
                                    "Median Q1 (tr)", "Median Q4 (tr)", "Q4/Q1"], rows))

# so sánh r gốc và r log cho vài cặp biến tiêu biểu + kiểm tra độ vững khi bỏ 1% cao nhất
rows = []
g14b = d[d.Year == 2014].copy()
for k, lab, per in [("house", "Giá trị nhà – thu nhập/người", False), ("tech", "Đồ công nghệ – thu nhập/người", False),
                    ("rice", "Chi gạo/người – thu nhập/người", True), ("nfood", "Chi ngoài ăn uống/người – thu nhập/người", True),
                    ("med", "Chi y tế/người – thu nhập/người", True)]:
    z = g14b[(g14b[k] > 0) & g14b.Inc_head.notna()]
    x = z[k]/z["size"] if per else z[k]
    r_raw = np.corrcoef(x, z.Inc_head)[0, 1]; r_log = np.corrcoef(np.log(x), np.log(z.Inc_head))[0, 1]
    cut = z.Inc_head.quantile(0.99); z2 = z[z.Inc_head <= cut]
    x2 = z2[k]/z2["size"] if per else z2[k]
    r_raw2 = np.corrcoef(x2, z2.Inc_head)[0, 1]; r_log2 = np.corrcoef(np.log(x2), np.log(z2.Inc_head))[0, 1]
    rows.append([lab, p(r_raw, 2), p(r_raw2, 2), p(r_log, 2), p(r_log2, 2)])
write("t_r_scale", tab("lrrrr", ["Cặp biến (năm 2014)", "r số gốc", "r số gốc, bỏ 1\\% thu nhập cao nhất",
                                 "r thang log", "r log, bỏ 1\\%"], rows))

# phụ lục: 63 tỉnh, chia hai khối cho vừa trang
rows = []
order = sorted(df.province_name.unique(), key=lambda nm: -df[df.province_name == nm].Inc_head.median())
for i, name in enumerate(order, 1):
    z = df[df.province_name == name]; zd = d[d.province_name == name]
    z14 = z[z.Year == 2014]
    rows.append([str(i), name, z.tier.iloc[0], vn(len(z)), p(z14.Inc_head.median()/M, 1),
                 p(z14[z14.house > 0].house.median()/M, 0), pc(zd.ov.mean()*100, 0)])
half = (len(rows) + 1)//2
head = ["\\#", "Tỉnh/TP", "Nhóm", "n", "Thu nhập 2014", "Giá nhà 2014", "\\% vượt thu"]
write("t_prov_a", tab("rllrrrr", head, rows[:half]))
write("t_prov_b", tab("rllrrrr", head, rows[half:]))

# ---------------------------------------------------------------- độ tin cậy của T1–T4
rng = np.random.default_rng(7)
df2 = df.copy(); df2["half"] = rng.integers(0, 2, len(df2))
def tier_of(sub):
    med = sub.groupby("province").Inc_head.median()
    return pd.qcut(med.rank(method="first"), 4, labels=["T1", "T2", "T3", "T4"])
tA, tB = tier_of(df2[df2.half == 0]), tier_of(df2[df2.half == 1])
same = (tA == tB).mean()*100
rA = df2[df2.half == 0].groupby("province").Inc_head.median()
rB = df2[df2.half == 1].groupby("province").Inc_head.median()
rho = np.corrcoef(rA.rank(), rB.rank())[0, 1]
N["splithalf"] = dict(same_tier=round(same), rank_corr=round(rho, 2))
# sai số chuẩn của tỷ lệ: tỉnh so với nhóm tỉnh
n_prov = d.groupby("province_name").size().median(); n_tier = d.groupby("tier").size().median()
N["se_prov"] = round(np.sqrt(0.5*0.5/n_prov)*100, 1); N["se_tier"] = round(np.sqrt(0.5*0.5/n_tier)*100, 1)
N["n_prov_med"] = int(n_prov); N["n_tier_med"] = int(n_tier)

json.dump(N, open(f"{ROOT}/presentation/analysis/numbersR.json", "w"), ensure_ascii=False, indent=1)
print("numbersR.json:", len(N), "mục |", "split-half:", N["splithalf"], "| SE tỉnh", N["se_prov"], "vs nhóm tỉnh", N["se_tier"])
