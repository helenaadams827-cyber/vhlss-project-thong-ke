# -*- coding: utf-8 -*-
"""Hình cho F2–F3: thu nhập có đủ trang trải chi tiêu thiết yếu của hộ nghèo (Q1) ở từng nơi không."""
import json, numpy as np, pandas as pd
from matplotlib.patches import Patch
from style import *

df = pd.read_csv(ROOT + "/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy()
d["short"] = d.nec > d.income          # chi thiết yếu vượt thu nhập: không đủ sống
d["over"] = d.tot > d.income           # tổng chi vượt thu nhập
q1 = d[d.Quart == 1]
Q = [1, 2, 3, 4]; TIERS = ["T1", "T2", "T3", "T4"]; AREAS = ["Thành thị", "Nông thôn"]; YRS = [2010, 2012, 2014]
SC = {"Toàn quốc": q1.area > 0, "Thành thị": q1.area == 1, "Nông thôn": q1.area == 2,
      "T1": q1.tier == "T1", "T2": q1.tier == "T2", "T3": q1.tier == "T3", "T4": q1.tier == "T4"}
SCL = ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"]
N = {}

def spread(vals, gap):
    order = np.argsort(vals); pos = np.array(vals, float)[order]
    for k in range(1, len(pos)): pos[k] = max(pos[k], pos[k - 1] + gap)
    pos += np.mean(vals) - pos.mean(); out = np.empty_like(pos); out[order] = pos; return out

# ---------------- F2: hộ Q1 không đủ trang trải thiết yếu, theo phạm vi và theo năm
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 1.9), gridspec_kw={"width_ratios": [1.15, 1]})
v = [q1[m].short.mean() * 100 for m in SC.values()]
r = bars(a, np.arange(7), v, [GRAY] * 3 + ORD4, width=0.6); label_bars(a, r, lambda z: vn(z) + "%", dy=1, size=6.2)
a.set_xticks(np.arange(7), SCL, fontsize=6); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 50)
a.set_title("% hộ Q1 chi thiết yếu > thu nhập")
ends = []
for ti, tt in enumerate(TIERS):
    vv = [q1[(q1.tier == tt) & (q1.Year == y)].short.mean() * 100 for y in YRS]; ends.append(vv[-1])
    b.plot(YRS, vv, color=ORD4[ti], marker="o", ms=4.5, mec=SURF, mew=1.2)
ly = spread(ends, 2.6)
for ti, tt in enumerate(TIERS): b.text(2014.3, ly[ti], f"{tt} {vn(ends[ti])}%", va="center", fontsize=6.3, color=INK2)
b.set_xticks(YRS, [str(y) for y in YRS]); b.set_xlim(2009.6, 2015.6); b.set_ylim(20, 50); b.yaxis.set_major_formatter(pct_fmt())
b.set_title("Theo năm")
plt.subplots_adjust(wspace=0.35); save(fig, "f33_F2")
yr = lambda m: [round(q1[m & (q1.Year == y)].short.mean() * 100, 1) for y in YRS]
N["F2"] = dict(short={k: round(q1[m].short.mean() * 100, 1) for k, m in SC.items()},
               over={k: round(q1[m].over.mean() * 100, 1) for k, m in SC.items()},
               n={k: int(m.sum()) for k, m in SC.items()},
               short_year={k: yr(m) for k, m in SC.items()},
               short_year_nofuelna=[round(q1[(q1.Year == y) & ~q1.fuel_na].short.mean() * 100, 1) for y in YRS],
               t4_2014_nofuelna=round(q1[(q1.Year == 2014) & ~q1.fuel_na & (q1.tier == "T4")].short.mean() * 100, 1),
               t1_2014_nofuelna=round(q1[(q1.Year == 2014) & ~q1.fuel_na & (q1.tier == "T1")].short.mean() * 100, 1),
               byQ={q: round(d[d.Quart == q].short.mean() * 100, 1) for q in Q},
               tier_area={f"{t}|{ar}": round(q1[(q1.tier == t) & (q1.area_l == ar)].short.mean() * 100, 1) for t in TIERS for ar in AREAS},
               inchead_q1={t: round(q1[q1.tier == t].Inc_head.median()) for t in TIERS},
               size_q1={t: round(q1[q1.tier == t]["size"].mean(), 2) for t in TIERS},
               nrice_inc={t: round((q1[q1.tier == t].nrice / q1[q1.tier == t].income).median() * 100, 1) for t in TIERS})

# ---------------- F3: từng tỉnh
pv = q1.groupby("province").agg(name=("province_name", "first"), tier=("tier", "first"), n=("short", "size"), short=("short", "mean"), over=("over", "mean"))
pv["short"] *= 100; pv["over"] *= 100
pv["inc14"] = df[df.Year == 2014].groupby("province").Inc_head.median() / 1000
pv["nall"] = df.groupby("province").size(); pv["q1share"] = pv.n / pv.nall * 100
ok = pv[pv.n >= 30]
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1.25, 1]})
a.scatter(ok.inc14, ok.short, s=ok.n * 0.45, color=[ORD4[TIERS.index(t)] for t in ok.tier], alpha=0.9, edgecolor=SURF, linewidth=0.8, zorder=3)
LAB = {1: (4, 4, "left"), 48: (4, 3, "left"), 92: (4, -8, "left"), 77: (5, -1, "left"), 70: (-5, 2, "right"), 64: (4, -3, "left")}
for pid, (dx, dy, ha) in LAB.items():
    if pid in ok.index: a.annotate(ok.loc[pid, "name"], (ok.loc[pid, "inc14"], ok.loc[pid, "short"]), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=6.6, color=INK2)
a.set_xlabel("Median Inc_head của tỉnh, 2014 (triệu đồng)"); a.yaxis.set_major_formatter(pct_fmt()); a.grid(True, axis="both"); a.set_ylim(0, 96)
a.set_title("61 tỉnh có ≥ 30 hộ Q1: % hộ Q1 thiếu hụt")
a.legend(handles=[Patch(color=c, label=l) for c, l in zip(ORD4, TIERS)], loc="upper left", fontsize=5.8, ncols=4)
a.text(0.02, 0.03, "kích thước = số hộ Q1; TP.HCM (5 hộ), Bình Dương (18) bị loại", transform=a.transAxes, fontsize=5.6, color=MUTED)
rk = pd.concat([ok.sort_values("short", ascending=False).head(6), ok.sort_values("short").head(6).iloc[::-1]])
y = np.arange(len(rk))[::-1] + np.r_[np.full(6, 0.6), np.zeros(6)]
hbars(b, y, rk.short.values, [ORD4[TIERS.index(t)] for t in rk.tier], height=0.62)
for yy, (vv, nn) in zip(y, zip(rk.short.values, rk.n.values)): b.text(vv + 1.5, yy, f"{vn(vv)}%  (n = {nn})", va="center", fontsize=5.8, color=INK2)
b.set_yticks(y, rk.name, fontsize=6.2); b.set_xlim(0, 110); b.set_xticks([]); b.grid(False)
b.set_title("Khó nhất (trên) và dễ nhất (dưới)")
plt.subplots_adjust(wspace=0.45); save(fig, "f34_F3")
se = lambda p, n: np.sqrt(p / 100 * (1 - p / 100) / n) * 100
five = {1: "Hà Nội", 79: "TP.HCM", 31: "Hải Phòng", 48: "Đà Nẵng", 92: "Cần Thơ"}
N["F3"] = dict(r=round(np.corrcoef(ok.inc14, ok.short)[0, 1], 2), n_ok=int(len(ok)),
               hardest=[(r_["name"], round(r_.short, 1), int(r_.n)) for _, r_ in ok.sort_values("short", ascending=False).head(6).iterrows()],
               easiest=[(r_["name"], round(r_.short, 1), int(r_.n)) for _, r_ in ok.sort_values("short").head(6).iterrows()],
               cities={five[p]: dict(short=round(pv.loc[p, "short"], 1), over=round(pv.loc[p, "over"], 1), n=int(pv.loc[p, "n"]), nall=int(pv.loc[p, "nall"]),
                                     q1share=round(pv.loc[p, "q1share"], 1), se=round(se(pv.loc[p, "short"], pv.loc[p, "n"]), 1)) for p in five},
               sd_prov=round(ok.short.std(), 1), mean_prov=round(ok.short.mean(), 1), min_n=int(ok.n.min()))
json.dump(N, open(ROOT + "/presentation/analysis/numbers3.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(N, ensure_ascii=False))

# =====================================================================
#  Lượt rà soát thêm: A3 (tỉnh), A4 (thập phân vị), C5 (heatmap chi tiêu), F4 (để dành)
# =====================================================================
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("pastelblue", ["#f4f7fd", "#bfd2f3", "#8dabe4", "#6380c8", "#41559e"])
YRS = [2010, 2012, 2014]

# ---------------- A3 mở rộng: CV theo phạm vi + 63 tỉnh (median và CV)
def cv_trim(x):
    s = np.sort(np.asarray(x, float)); s = s[:max(2, int(len(s) * 0.99))]; return s.std(ddof=1) / s.mean()
SCOPE = [("Toàn quốc", df.area > 0), ("Thành thị", df.area == 1), ("Nông thôn", df.area == 2)] + [(t, df.tier == t) for t in TIERS]
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1.25, 1]})
for yi, y in enumerate(YRS):
    v = [cv_trim(df[m & (df.Year == y)].Inc_head) for _, m in SCOPE]
    bars(a, np.arange(7) + (yi - 1) * 0.26, v, ORD3[yi], width=0.25, label=str(y))
a.set_xticks(np.arange(7), ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"], fontsize=6.4); a.yaxis.set_major_formatter(num_fmt(1))
a.set_title("CV của thu nhập/người (bỏ 1% hộ cao nhất)"); a.legend(loc="upper right", ncols=3, fontsize=6.2); a.set_ylim(0, 1.0)
pv = pd.DataFrame([(p, g.province_name.iloc[0], g.tier.iloc[0], g.Inc_head.median() / 1000, cv_trim(g.Inc_head))
                   for p, g in df[df.Year == 2014].groupby("province")], columns=["p", "name", "tier", "med", "cv"])
b.scatter(pv.med, pv.cv, s=16, color=[ORD4[TIERS.index(t)] for t in pv.tier], edgecolor=SURF, linewidth=0.8, zorder=3)
b.set_xscale("log"); b.xaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(v))); b.xaxis.set_minor_formatter(FuncFormatter(lambda v, p: ""))
b.set_xticks([10, 20, 40]); b.grid(True, axis="both")
for nm, dx, dy, ha in [("Sơn La", 5, 0, "left"), ("Điện Biên", 5, -2, "left"), ("TP.HCM", 6, 3, "left"), ("Hà Nội", -6, -9, "right")]:
    r_ = pv[pv.name == nm].iloc[0]; b.annotate(nm, (r_.med, r_.cv), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=6.2, color=INK2)
rr = {y: np.corrcoef(np.log([g.Inc_head.median() for _, g in df[df.Year == y].groupby("province")]), [cv_trim(g.Inc_head) for _, g in df[df.Year == y].groupby("province")])[0, 1] for y in YRS}

b.set_title(f"63 tỉnh 2014: r(ln median, CV) = {vn(rr[2014], 2)}", fontsize=7.4); b.set_xlabel("Median thu nhập/người (triệu, log)"); b.set_ylabel("CV", fontsize=6.5)
plt.subplots_adjust(wspace=0.3); save(fig, "f07w_A3")
N["A3w"] = dict(r_prov={y: round(v, 2) for y, v in rr.items()}, top_cv=pv.sort_values("cv", ascending=False).head(4)[["name", "cv"]].round(2).values.tolist(),
                low_cv=pv.sort_values("cv").head(4)[["name", "cv"]].round(2).values.tolist())

# ---------------- A4: thu nhập chia theo 10 nhóm (thập phân vị Inc_head trong từng năm)
def dec_share(g):
    g = g.assign(dec=pd.qcut(g.Inc_head.rank(method="first"), 10, labels=False) + 1)
    return g.groupby("dec").income.sum() / g.income.sum() * 100, g.groupby("dec")["size"].sum() / g["size"].sum() * 100
sh14, pop14 = dec_share(df[df.Year == 2014])
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1.3, 1]})
cols = [ORD4[0]] * 4 + [GRAY] * 5 + [ORD4[3]]
r = bars(a, np.arange(10), sh14.values, cols, width=0.7); label_bars(a, r, lambda z: vn(z, 1), dy=0.4, size=6)
a.set_xticks(np.arange(10), [f"D{k}" for k in range(1, 11)], fontsize=6.4); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 31)
a.set_title("% tổng thu nhập của mỗi 10% hộ, 2014"); a.set_xlabel("D1 = 10% hộ có thu nhập/người thấp nhất … D10 = cao nhất", fontsize=6.2)
tops, bots = [], []
for y in YRS:
    s_, _ = dec_share(df[df.Year == y]); tops.append(s_[10]); bots.append(s_.loc[1:4].sum())
b.plot(YRS, tops, color=ORD4[3], marker="o", ms=4.5, mec=SURF, mew=1.2); b.plot(YRS, bots, color=ORD4[0], marker="o", ms=4.5, mec=SURF, mew=1.2)
b.text(2014.3, tops[-1], "10% giàu nhất " + vn(tops[-1], 1) + "%", va="center", fontsize=6.2, color=INK2)
b.text(2014.3, bots[-1], "40% nghèo nhất " + vn(bots[-1], 1) + "%", va="center", fontsize=6.2, color=INK2)
for x, v in zip(YRS, tops): b.text(x, v + 0.9, vn(v, 1), ha="center", fontsize=5.8, color=INK2)
b.set_xticks(YRS, [str(y) for y in YRS]); b.set_xlim(2009.6, 2017.2); b.set_ylim(10, 33); b.yaxis.set_major_formatter(pct_fmt()); b.set_title("% tổng thu nhập, theo năm")
plt.subplots_adjust(wspace=0.3); save(fig, "f35_A4")
def shares_of(mask):
    s_, _ = dec_share(df[mask & (df.Year == 2014)]); return round(s_[10], 1), round(s_.loc[1:4].sum(), 1)
N["A4"] = dict(dec14={int(k): round(v, 1) for k, v in sh14.items()}, pop_top=round(pop14[10], 1), pop_bot=round(pop14.loc[1:4].sum(), 1),
               top=[round(v, 1) for v in tops], bot=[round(v, 1) for v in bots], ratio=[round(t / b_, 2) for t, b_ in zip(tops, bots)],
               scopes={n: shares_of(m) for n, m in SCOPE})

# ---------------- C5: heatmap tương quan giữa từng khoản chi/người và thu nhập/người
ITEMS = {"ngoài ăn uống": "nfood", "thực phẩm khác gạo": "nrice", "điện": "elec", "nhiên liệu": "fuel", "giáo dục": "edu", "nước": "water",
         "sửa nhà": "fhouse", "hỗ trợ KCB": "aid", "phí rác": "garb", "thuốc, viện phí": "med", "thuốc lá": "tobaco", "BHYT": "hins", "gạo": "rice"}
dd = d.copy()
COLS = [("Toàn quốc", dd.Year == 2014), ("Thành thị", (dd.Year == 2014) & (dd.area == 1)), ("Nông thôn", (dd.Year == 2014) & (dd.area == 2))] + \
       [(t, (dd.Year == 2014) & (dd.tier == t)) for t in TIERS] + [(str(y), dd.Year == y) for y in YRS]
def rc(mask, k):
    z = dd[mask & (dd[k] > 0)]
    return np.corrcoef(np.log(z[k] / z["size"]), np.log(z.Inc_head))[0, 1] if len(z) >= 30 else np.nan
M = pd.DataFrame({c: {l: rc(m, k) for l, k in ITEMS.items()} for c, m in COLS}).sort_values("Toàn quốc", ascending=False)
own = {l: (dd[dd.Year == 2014][ITEMS[l]] > 0).mean() * 100 for l in M.index}
fig, a = plt.subplots(figsize=(5.9, 2.6))
xs = [0, 1.25, 2.25, 3.5, 4.5, 5.5, 6.5, 7.75, 8.75, 9.75]
for i, l in enumerate(M.index):
    for j, c in enumerate(M.columns):
        v = M.loc[l, c]; col = cmap(np.clip(v / 0.75, 0, 1)) if v == v else LIGHTGRAY
        a.add_patch(plt.Rectangle((xs[j] - 0.47, i - 0.44), 0.94, 0.88, color=col, lw=0))
        a.text(xs[j], i, (vn(0.0, 2) if abs(v) < 0.005 else vn(v, 2)) if v == v else "–", ha="center", va="center", fontsize=6.1, color="white" if v == v and v > 0.55 else INK)
    a.text(11.0, i, vn(own[l]) + "%", ha="center", va="center", fontsize=6.2, color=INK2)
a.set_xlim(-0.6, 11.6); a.set_ylim(len(M) - 0.5, -2.75); a.set_yticks(np.arange(len(M)), list(M.index), fontsize=6.6); a.set_xticks([])
for x, hd in zip(xs + [11.0], ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4", "2010", "2012", "2014", "% hộ\ncó chi"]):
    a.text(x, -0.62, hd, ha="center", va="bottom", fontsize=6.2, color=INK2, linespacing=1.0)
a.grid(False); [sp.set_visible(False) for sp in a.spines.values()]
for x0, x1, lab in [(-0.47, 0.47, "2014"), (0.78, 2.72, "2014 · khu vực"), (3.03, 6.97, "2014 · nhóm tỉnh"), (7.28, 10.22, "toàn quốc · theo năm"), (10.55, 11.45, "2014")]:
    a.plot([x0, x1], [-2.05, -2.05], color=BASE, lw=0.8); a.text((x0 + x1) / 2, -2.15, lab, ha="center", va="bottom", fontsize=5.8, color=MUTED)
save(fig, "f36_C5")
N["C5"] = {l: {c: (None if M.loc[l, c] != M.loc[l, c] else round(M.loc[l, c], 2)) for c in M.columns} for l in M.index}
N["C5_own"] = {l: round(v) for l, v in own.items()}

# ---------------- F4: tỷ lệ để dành = (thu nhập − tổng chi) / thu nhập
dd["save"] = (dd.income - dd.tot) / dd.income * 100
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1.1, 1]})
for i, ar in enumerate(AREAS):
    v = [dd[(dd.Quart == q) & (dd.area_l == ar)].save.median() for q in Q]
    r = bars(a, np.arange(4) + (i - 0.5) * 0.36, v, AREA[ar], width=0.34, label=ar)
    for x_, v_ in zip(np.arange(4) + (i - 0.5) * 0.36, v): a.text(x_, v_ + (1.5 if v_ >= 0 else -2), vn(v_), ha="center", va="bottom" if v_ >= 0 else "top", fontsize=6, color=INK2)
a.axhline(0, color=BASE, lw=0.8); a.set_xticks(np.arange(4), ["Q1", "Q2", "Q3", "Q4"]); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(-25, 55)
a.set_title("Median % thu nhập để dành (gộp 3 năm)"); a.legend(loc="upper left", fontsize=6.2); a.set_ylim(-30, 55)
ends = []
for qi, q in enumerate(Q):
    v = [dd[(dd.Quart == q) & (dd.Year == y)].save.median() for y in YRS]; ends.append(v[-1])
    b.plot(YRS, v, color=ORD4[qi], marker="o", ms=4.5, mec=SURF, mew=1.2)
for qi in range(4): b.text(2014.3, ends[qi], f"Q{qi + 1} {vn(ends[qi])}%", va="center", fontsize=6.2, color=INK2)
b.axhline(0, color=BASE, lw=0.8); b.set_xticks(YRS, [str(y) for y in YRS]); b.set_xlim(2009.6, 2015.9); b.yaxis.set_major_formatter(pct_fmt()); b.set_title("Theo năm")
plt.subplots_adjust(wspace=0.3); save(fig, "f37_F4")
N["F4"] = dict(q={q: round(dd[dd.Quart == q].save.median(), 1) for q in Q},
               area={ar: [round(dd[(dd.Quart == q) & (dd.area_l == ar)].save.median(), 1) for q in Q] for ar in AREAS},
               year={q: [round(dd[(dd.Quart == q) & (dd.Year == y)].save.median(), 1) for y in YRS] for q in Q},
               tier={t: [round(dd[(dd.Quart == q) & (dd.tier == t)].save.median(), 1) for q in Q] for t in TIERS},
               sumshare={q: round((1 - dd[dd.Quart == q].tot.sum() / dd[dd.Quart == q].income.sum()) * 100, 1) for q in Q})

# ---------------- các số bổ sung cho thẻ nhận xét
e = dd[dd.edu > 0]; hh = df[df.house.notna() & (df.house > 0)]
N["extra"] = dict(
    edu_pc={q: round((e[e.Quart == q].edu / e[e.Quart == q]["size"]).median()) for q in Q},
    cat10={q: round((dd[dd.Quart == q].med / dd[dd.Quart == q].tot > 0.10).mean() * 100, 1) for q in Q},
    cat25=round((dd.med / dd.tot > 0.25).mean() * 100, 1),
    tob_edu={q: round(dd[dd.Quart == q].tobaco.sum() / dd[dd.Quart == q].edu.sum() * 100) for q in Q},
    tob_gt_edu_both={q: round(((lambda z: (z.tobaco > z.edu).mean())(dd[(dd.Quart == q) & (dd.tobaco > 0) & (dd.edu > 0)])) * 100) for q in Q},
    tele_gap={y: round(((df[(df.Year == y) & (df.Quart == 4)].tele > 0).mean() - (df[(df.Year == y) & (df.Quart == 1)].tele > 0).mean()) * 100) for y in YRS},
    tv_gap={y: round(((df[(df.Year == y) & (df.Quart == 4)].tv > 0).mean() - (df[(df.Year == y) & (df.Quart == 1)].tv > 0).mean()) * 100) for y in YRS},
    hti={f"{a_}-{q}": [round(hh[(hh.Year == y) & (hh.area == a_) & (hh.Quart == q)].house_to_inc.median(), 1) for y in YRS] for a_ in [1, 2] for q in Q},
    size7_q1=round((df[df["size"] >= 7].Quart == 1).mean() * 100),
)
json.dump(N, open(ROOT + "/presentation/analysis/numbers3.json", "w"), ensure_ascii=False, indent=1)

# ---------------- C5 bản cho slide: chỉ 7 phạm vi 2014 + % hộ có chi (đặt cạnh thẻ)
fig, a = plt.subplots(figsize=(3.9, 2.9))
xs2 = [0, 1.15, 2.15, 3.3, 4.3, 5.3, 6.3]
for i, l in enumerate(M.index):
    for j, c in enumerate(M.columns[:7]):
        v = M.loc[l, c]; col = cmap(np.clip(v / 0.75, 0, 1)) if v == v else LIGHTGRAY
        a.add_patch(plt.Rectangle((xs2[j] - 0.47, i - 0.44), 0.94, 0.88, color=col, lw=0))
        a.text(xs2[j], i, (vn(0.0, 2) if abs(v) < 0.005 else vn(v, 2)), ha="center", va="center", fontsize=6.3, color="white" if v > 0.55 else INK)
    a.text(7.45, i, vn(own[l]) + "%", ha="center", va="center", fontsize=6.3, color=INK2)
a.set_xlim(-0.6, 8.0); a.set_ylim(len(M) - 0.5, -2.2); a.set_yticks(np.arange(len(M)), list(M.index), fontsize=6.8); a.set_xticks([])
for x, hd in zip(xs2 + [7.45], ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4", "% hộ\ncó chi"]):
    a.text(x, -0.62, hd, ha="center", va="bottom", fontsize=6.3, color=INK2, linespacing=1.0)
a.grid(False); [sp.set_visible(False) for sp in a.spines.values()]
save(fig, "f36s_C5")

# =====================================================================
#  Xu hướng liên tục 2010 → 2012 → 2014
# =====================================================================
# ---------------- E1: lưới xu hướng (3 phạm vi × 4 chỉ số)
IND = [("Median thu nhập/người\n(triệu đồng)", lambda g: g.Inc_head.median() / 1000, "num"),
       ("% chi cho thiết yếu", lambda g: g.nec.sum() / g.tot.sum() * 100, "pct"),
       ("Tỷ trọng gạo trong tổng chi", lambda g: g.rice.sum() / g.tot.sum() * 100, "pct"),
       ("% hộ có điện thoại", lambda g: (g.tele > 0).mean() * 100, "pct")]
ROWS = [("Theo Q", "Quart", [1, 2, 3, 4], ORD4, ["Q1", "Q2", "Q3", "Q4"]),
        ("Khu vực", "area_l", AREAS, [BLUE, CORAL], ["TT", "NT"]),
        ("Nhóm tỉnh", "tier", TIERS, ORD4, TIERS)]
fig, axs = plt.subplots(3, 4, figsize=(5.9, 2.5), sharex=True)
TG = {}
for ri, (rl, col, keys, cols, labs) in enumerate(ROWS):
    for ci, (il, f, kind) in enumerate(IND):
        ax = axs[ri, ci]; ends = []
        for k, c, lb in zip(keys, cols, labs):
            v = [f(dd[(dd.Year == y) & (dd[col] == k)]) for y in YRS]
            ax.plot(YRS, v, color=c, lw=1.8, marker="o", ms=3, mec=SURF, mew=0.8); ends.append((v[-1], lb, c))
            TG[f"{rl}|{il.split(chr(10))[0]}|{lb}"] = [round(x, 1) for x in v]
        ax.set_xticks(YRS, ["10", "12", "14"], fontsize=6); ax.tick_params(axis="y", labelsize=5.8)
        from matplotlib.ticker import MaxNLocator; ax.yaxis.set_major_locator(MaxNLocator(3))
        ax.margins(y=0.18)
        ax.yaxis.set_major_formatter(pct_fmt() if kind == "pct" else num_fmt()); ax.set_xlim(2009.5, 2015.6 if ci == 3 else 2014.5)
        if ri == 0: ax.set_title(il, fontsize=6.8, loc="left")
        if ci == 0: ax.set_ylabel(rl, fontsize=6.4, color=INK2)
        if ci == 3:
            ends.sort(); lo_, hi_ = ax.get_ylim(); ys_ = spread([e[0] for e in ends], (hi_ - lo_) * 0.24)
            if ys_.max() > hi_ - (hi_ - lo_) * 0.08: ys_ -= ys_.max() - (hi_ - (hi_ - lo_) * 0.08)
            for (v, lb, c), yy in zip(ends, ys_): ax.text(2014.35, yy, lb, fontsize=5.4, color=INK2, va="center")
plt.subplots_adjust(hspace=0.45, wspace=0.5); save(fig, "f38_E1grid")
N["E1grid"] = TG

# ---------------- E4b: thứ hạng của các tỉnh leo/tụt nhiều nhất qua 3 năm (hạng 1 = median cao nhất)
pm = df.groupby(["Year", "province"]).Inc_head.median().unstack(0)
rk = pm.rank(ascending=False)
names = df.groupby("province").province_name.first()
move = (rk[2010] - rk[2014]).sort_values()
sel = list(move.head(5).index) + list(move.tail(5).index)
fig, a = plt.subplots(figsize=(3.7, 2.9))
for p in sel:
    up = move[p] > 0; c = BLUE if up else CORAL
    a.plot(YRS, rk.loc[p, YRS], color=c, lw=1.8, marker="o", ms=3.5, mec=SURF, mew=0.8)
yr_ = spread([rk.loc[p, 2014] for p in sel], 2.8); yl_ = spread([rk.loc[p, 2010] for p in sel], 2.8)
for p, y1_, y0_ in zip(sel, yr_, yl_):
    a.text(2014.25, y1_, f"{names[p]} {int(rk.loc[p, 2010])}→{int(rk.loc[p, 2014])}", va="center", fontsize=5.8, color=INK2)
    a.text(2009.75, y0_, names[p], va="center", ha="right", fontsize=5.4, color=MUTED)
a.set_ylim(60, -2); a.set_xticks(YRS, [str(y) for y in YRS]); a.set_xlim(2008.0, 2016.6); a.set_ylabel("Hạng (1 = cao nhất)", fontsize=6.4)
a.set_title("Thứ hạng median thu nhập/người: 5 tỉnh leo, 5 tỉnh tụt nhiều nhất", fontsize=7)
a.grid(True, axis="y")
save(fig, "f26b_E4")
N["E4rank"] = {names[p]: [int(rk.loc[p, y]) for y in YRS] for p in sel}

# ---------------- E5: cái gì thay đổi nhiều nhất 2010 → 2014 (điểm đầu → điểm cuối)
SP = {"TP khác gạo": "nrice", "ngoài ăn uống": "nfood", "gạo": "rice", "nhiên liệu*": "fuel", "thuốc, viện phí": "med", "giáo dục": "edu",
      "điện": "elec", "sửa nhà": "fhouse", "BHYT": "hins", "thuốc lá": "tobaco", "hỗ trợ KCB": "aid", "nước": "water", "phí rác": "garb"}
OW = {"điện thoại": "tele", "xe máy": "moto", "máy gia dụng": "hmachine", "TV": "tv", "máy giải trí": "emachine", "xe đạp": "bicycle", "ô tô": "oto"}   # giường, bàn ghế: năm 2010 ghi khác, bỏ
s10 = {l: dd[dd.Year == 2010][k].sum() / dd[dd.Year == 2010].tot.sum() * 100 for l, k in SP.items()}
s14 = {l: dd[dd.Year == 2014][k].sum() / dd[dd.Year == 2014].tot.sum() * 100 for l, k in SP.items()}
o10 = {l: (df[df.Year == 2010][k] > 0).mean() * 100 for l, k in OW.items()}
o14 = {l: (df[df.Year == 2014][k] > 0).mean() * 100 for l, k in OW.items()}
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.15), gridspec_kw={"width_ratios": [1, 1]})
for ax, A0, A1, ttl, unit in [(a, s10, s14, "Tỷ trọng trong tổng chi", "điểm"), (b, o10, o14, "% hộ có món đồ", "điểm")]:
    order = sorted(A0, key=lambda l: A1[l] - A0[l])
    for i, l in enumerate(order):
        d0, d1 = A0[l], A1[l]; c = BLUE if d1 >= d0 else CORAL
        ax.annotate("", xy=(d1, i), xytext=(d0, i), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.4, mutation_scale=7))
        ax.plot([d0], [i], "o", ms=3.2, color=GRAY, mec=SURF, mew=0.6, zorder=3)
        ax.text(max(d0, d1) + (ax is a and 0.6 or 2), i, ("+" if d1 >= d0 else "−") + vn(abs(d1 - d0), 1), va="center", fontsize=5.8, color=INK2)
    ax.set_yticks(np.arange(len(order)), order, fontsize=6.3); ax.grid(True, axis="x"); ax.grid(False, axis="y")
    ax.xaxis.set_major_formatter(pct_fmt()); ax.set_title(ttl + ": 2010 ● → 2014", fontsize=7.2)
a.set_xlim(0, 50); b.set_xlim(0, 108)
plt.subplots_adjust(wspace=0.55); save(fig, "f39_E5")
N["E5"] = dict(spend={l: [round(s10[l], 1), round(s14[l], 1)] for l in SP}, own={l: [round(o10[l], 1), round(o14[l], 1)] for l in OW})

# ---------------- A3 (bản đường): CV đã bỏ 1% qua 3 năm, mỗi phạm vi một đường
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1.05, 1]})
LN = [("Toàn quốc", df.area > 0, INK2, (0, (3, 2))), ("Thành thị", df.area == 1, BLUE, "-"), ("Nông thôn", df.area == 2, CORAL, "-")] + [(t, df.tier == t, ORD4[i], "-") for i, t in enumerate(TIERS)]
ends = []
for nm, m, c, ls in LN:
    v = [cv_trim(df[m & (df.Year == y)].Inc_head) for y in YRS]
    a.plot(YRS, v, color=c, lw=1.8, ls=ls, marker="o", ms=3.2, mec=SURF, mew=0.8); ends.append((v[-1], nm))
ys_ = spread([e[0] for e in ends], 0.022)
for (v, nm), yy in zip(ends, ys_): a.text(2014.3, yy, nm, va="center", fontsize=5.9, color=INK2)
a.set_xticks(YRS, [str(y) for y in YRS]); a.set_xlim(2009.6, 2016.2); a.yaxis.set_major_formatter(num_fmt(2)); a.set_title("CV (bỏ 1% hộ cao nhất), 2010 → 2014", fontsize=7.2)
b.scatter(pv.med, pv.cv, s=16, color=[ORD4[TIERS.index(t)] for t in pv.tier], edgecolor=SURF, linewidth=0.8, zorder=3)
b.set_xscale("log"); b.xaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(v))); b.xaxis.set_minor_formatter(FuncFormatter(lambda v, p: "")); b.set_xticks([10, 20, 40]); b.grid(True, axis="both")
for nm, dx, dy, ha in [("Sơn La", 5, 0, "left"), ("Điện Biên", 5, -2, "left"), ("TP.HCM", 6, 3, "left"), ("Hà Nội", -6, -9, "right")]:
    r_ = pv[pv.name == nm].iloc[0]; b.annotate(nm, (r_.med, r_.cv), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=6.2, color=INK2)
b.set_title(f"63 tỉnh 2014: r(ln median, CV) = {vn(rr[2014], 2)}", fontsize=7.2); b.set_xlabel("Median thu nhập/người (triệu, log)"); b.set_ylabel("CV", fontsize=6.5)
plt.subplots_adjust(wspace=0.3); save(fig, "f07w_A3")
N["A3lines"] = {nm: [round(cv_trim(df[m & (df.Year == y)].Inc_head), 3) for y in YRS] for nm, m, _, _ in LN}
json.dump(N, open(ROOT + "/presentation/analysis/numbers3.json", "w"), ensure_ascii=False, indent=1)

# =====================================================================
#  Panel xu hướng cho các mục có insight theo thời gian (bản *_t dùng trên slide)
# =====================================================================
def trend_lines(ax, col, keys, colors, labels, f, fmt="pct", data=None, gap=None, suffix=None):
    data = dd if data is None else data; ends = []
    for k, c, lb in zip(keys, colors, labels):
        v = [f(data[(data.Year == y) & (data[col] == k)]) for y in YRS]
        ax.plot(YRS, v, color=c, lw=2, marker="o", ms=4, mec=SURF, mew=1.1); ends.append((v[-1], lb + (suffix(v) if suffix else "")))
    lo, hi = ax.get_ylim(); ys_ = spread([e[0] for e in ends], gap or (hi - lo) * 0.09)
    for (v, lb), yy in zip(ends, ys_): ax.text(2014.3, yy, lb, va="center", fontsize=6, color=INK2)
    ax.set_xticks(YRS, [str(y) for y in YRS]); ax.set_xlim(2009.6, 2016.3)
    ax.yaxis.set_major_formatter(pct_fmt() if fmt == "pct" else num_fmt())
QL_ = ["Q1", "Q2", "Q3", "Q4"]
SCL_ = ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"]
def scope_masks(g): return [g.area > 0, g.area == 1, g.area == 2] + [g.tier == t for t in TIERS]

# ---- B2: gánh nặng thiết yếu theo năm + riêng Q1 theo nơi ở
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.2]})
trend_lines(a, "Quart", Q, ORD4, [f"{q} " for q in QL_], lambda g: g.burden.median() * 100, suffix=lambda v: vn(v[-1]) + "%")
a.set_title("Median thiết yếu / thu nhập")
e14 = dd[dd.Year == 2014]
v = [e14[m & (e14.Quart == 1)].burden.median() * 100 for m in scope_masks(e14)]
r = bars(b, np.arange(7), v, [GRAY] * 3 + ORD4, width=0.6); label_bars(b, r, lambda z: vn(z) + "%", dy=1.5, size=6)
b.set_xticks(np.arange(7), SCL_, fontsize=6); b.yaxis.set_major_formatter(pct_fmt()); b.set_ylim(0, 105); b.set_title("Riêng hộ Q1, 2014: theo nơi ở")
plt.subplots_adjust(wspace=0.38); save(fig, "f10t_B2")

# ---- C2: tiền điện/người theo năm + nước, rác theo nơi ở
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.95), gridspec_kw={"width_ratios": [1.2, 1, 1]})
trend_lines(axs[0], "Quart", Q, ORD4, QL_, lambda g: (g.elec / g["size"]).median(), fmt="num", suffix=lambda v: " ×" + vn(v[-1] / v[0], 1))
axs[0].set_title("Median tiền điện/người (nghìn)"); axs[0].set_ylim(0, 1100)
for ax, colx, ttl in [(axs[1], "water", "% hộ trả tiền nước"), (axs[2], "garb", "% hộ trả phí rác")]:
    for i, ar in enumerate(AREAS):
        vv = [(dd[(dd.Quart == q) & (dd.area_l == ar)][colx] > 0).mean() * 100 for q in Q]
        bars(ax, np.arange(4) + (i - 0.5) * 0.36, vv, AREA[ar], width=0.34, label=ar)
    ax.set_title(ttl); ax.yaxis.set_major_formatter(pct_fmt()); ax.set_ylim(0, 100); ax.set_xticks(np.arange(4), QL_)
axs[1].legend(loc="upper left", fontsize=6)
plt.subplots_adjust(wspace=0.5); save(fig, "f14t_C2")

# ---- C4: ngoài ăn uống, thuốc lá theo khu vực, % hộ có chi thuốc lá theo năm
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.95), gridspec_kw={"width_ratios": [0.9, 1, 1.15]})
v = [dd[dd.Quart == q].nfood.sum() / dd[dd.Quart == q].tot.sum() * 100 for q in Q]
r = bars(axs[0], np.arange(4), v, ORD4, width=0.55); label_bars(axs[0], r, lambda z: vn(z, 1) + "%", dy=0.4, size=5.8)
axs[0].set_title("Ngoài ăn uống / tổng chi"); axs[0].set_ylim(0, 30); axs[0].yaxis.set_major_formatter(pct_fmt()); axs[0].set_xticks(np.arange(4), QL_)
for i, ar in enumerate(AREAS):
    vv = [dd[(dd.Quart == q) & (dd.area_l == ar)].tobaco.sum() / dd[(dd.Quart == q) & (dd.area_l == ar)].tot.sum() * 100 for q in Q]
    bars(axs[1], np.arange(4) + (i - 0.5) * 0.36, vv, AREA[ar], width=0.34, label=ar)
axs[1].set_title("Thuốc lá / tổng chi"); axs[1].yaxis.set_major_formatter(pct_fmt(1)); axs[1].legend(loc="upper right", fontsize=5.8); axs[1].set_ylim(0, 1.8); axs[1].set_xticks(np.arange(4), QL_)
trend_lines(axs[2], "Quart", Q, ORD4, QL_, lambda g: (g.tobaco > 0).mean() * 100)
axs[2].set_title("% hộ có chi thuốc lá")
plt.subplots_adjust(wspace=0.62); save(fig, "f16t_C4")

# ---- D2: đồ công nghệ Q1/Q4 theo nơi ở + median theo Q qua các năm
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1.35, 1]})
g14 = df[df.Year == 2014]
v1 = [g14[m & (g14.Quart == 1)].tech.median() / 1000 for m in scope_masks(g14)]
v4 = [g14[m & (g14.Quart == 4)].tech.median() / 1000 for m in scope_masks(g14)]
r1 = bars(a, np.arange(7) - 0.18, v1, ORD4[0], width=0.34, label="Hộ Q1"); r4 = bars(a, np.arange(7) + 0.18, v4, ORD4[3], width=0.34, label="Hộ Q4")
label_bars(a, r1, lambda z: vn(z, 1), dy=0.08, size=5.6); label_bars(a, r4, lambda z: vn(z, 1), dy=0.08, size=5.6)
a.set_xticks(np.arange(7), SCL_, fontsize=6); a.set_title("Median đồ công nghệ 2014 (triệu)"); a.legend(loc="upper left", ncols=2, fontsize=6); a.set_ylim(0, 7.2)
trend_lines(b, "Quart", Q, ORD4, QL_, lambda g: g.tech.median() / 1000, fmt="num", data=df, suffix=lambda v: " " + vn(v[-1], 1))
b.yaxis.set_major_formatter(num_fmt(1)); b.set_title("Median đồ công nghệ (triệu), 2010 → 2014")
plt.subplots_adjust(wspace=0.3); save(fig, "f18t_D2")

# ---- I1–I2: % tự đóng BHYT theo năm + chi y tế/thu nhập theo có/không BHYT
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 1.95))
trend_lines(a, "Quart", Q, ORD4, QL_, lambda g: (g.hins > 0).mean() * 100)
a.set_title("% hộ tự đóng BHYT, 2010 → 2014"); a.set_ylim(10, 70)
mi = dd.assign(mi=dd.med / dd.income * 100)
for i, (lab, m, c) in enumerate([("Có tự đóng BHYT", mi.hins > 0, VIOLET), ("Không tự đóng", mi.hins == 0, GRAY)]):
    vv = [mi[m & (mi.Quart == q)].mi.median() for q in Q]
    r = bars(b, np.arange(4) + (i - 0.5) * 0.36, vv, c, width=0.34, label=lab); label_bars(b, r, lambda z: vn(z, 1), dy=0.05, size=5.8)
b.set_xticks(np.arange(4), QL_); b.set_title("Median chi thuốc, viện phí / thu nhập"); b.yaxis.set_major_formatter(pct_fmt(1)); b.set_ylim(0, 4.6); b.legend(loc="upper right", fontsize=6)
plt.subplots_adjust(wspace=0.3); save(fig, "f28t_I12")

# ---- I9–I11: % chi > thu theo năm + hộ Q1 có từng món + hộ Q4 có ô tô
fig, axs = plt.subplots(1, 3, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1.1, 1.05, 0.7]})
trend_lines(axs[0], "Quart", Q, ORD4, QL_, lambda g: (g.tot > g.income).mean() * 100, suffix=lambda v: " " + vn(v[-1]) + "%")
axs[0].set_title("% hộ chi > thu nhập"); axs[0].set_ylim(0, 75)
a1214 = df[df.Year >= 2012]; q1 = a1214[a1214.Quart == 1]
ow = pd.Series({l: (q1[k] > 0).mean() * 100 for k, l in [("hmachine", "máy gia dụng"), ("bed", "giường"), ("tv", "TV"), ("tele", "điện thoại"), ("moto", "xe máy"), ("tab", "bàn ghế"), ("bicycle", "xe đạp"), ("emachine", "máy giải trí"), ("oto", "ô tô")]}).sort_values()
r = hbars(axs[1], np.arange(len(ow)), ow.values, [CORAL if l == "TV" else BLUE for l in ow.index], height=0.6); label_bars(axs[1], r, lambda z: vn(z) + "%", dy=1.5, size=5.8, horizontal=True)
axs[1].set_yticks(np.arange(len(ow)), ow.index, fontsize=6); axs[1].set_xlim(0, 100); axs[1].grid(False); axs[1].set_xticks([]); axs[1].set_title("Hộ Q1 có từng món")
v = [(a1214[(a1214.Quart == 4) & (a1214.tier == tt)].oto > 0).mean() * 100 for tt in TIERS]
r = bars(axs[2], np.arange(4), v, ORD4, width=0.55); label_bars(axs[2], r, lambda z: vn(z, 1) + "%", dy=0.15, size=5.8)
axs[2].set_xticks(np.arange(4), TIERS); axs[2].set_title("Hộ Q4 có ô tô"); axs[2].yaxis.set_major_formatter(pct_fmt()); axs[2].set_ylim(0, 9)
plt.subplots_adjust(wspace=0.75); save(fig, "f32t_I9")

# ---- số liệu xu hướng cho thẻ nhận xét và web
yr = lambda f, g=dd: [round(f(g[g.Year == y]), 1) for y in YRS]
N["trends"] = dict(
    burden={q: yr(lambda g: g[g.Quart == q].burden.median() * 100) for q in Q},
    rice_nec={q: yr(lambda g: g[g.Quart == q].rice.sum() / g[g.Quart == q].nec.sum() * 100) for q in Q},
    elec_pc={q: yr(lambda g: (g[g.Quart == q].elec / g[g.Quart == q]["size"]).median()) for q in Q},
    edu_gap=yr(lambda g: (g[(g.Quart == 4) & (g.edu > 0)].edu / g[(g.Quart == 4) & (g.edu > 0)]["size"]).median() / (g[(g.Quart == 1) & (g.edu > 0)].edu / g[(g.Quart == 1) & (g.edu > 0)]["size"]).median()),
    smoke={q: yr(lambda g: (g[g.Quart == q].tobaco > 0).mean() * 100) for q in Q},
    tech={q: yr(lambda g: g[g.Quart == q].tech.median() / 1000, df) for q in Q},
    moto={q: yr(lambda g: (g[g.Quart == q].moto > 0).mean() * 100, df) for q in Q},
    bhyt={q: yr(lambda g: (g[g.Quart == q].hins > 0).mean() * 100) for q in Q},
    overspend={q: yr(lambda g: (g[g.Quart == q].tot > g[g.Quart == q].income).mean() * 100) for q in Q},
    garb_tier={t: yr(lambda g: (g[g.tier == t].garb > 0).mean() * 100) for t in TIERS},
    q4q1=yr(lambda g: g[g.Quart == 4].Inc_head.median() / g[g.Quart == 1].Inc_head.median(), df),
)
json.dump(N, open(ROOT + "/presentation/analysis/numbers3.json", "w"), ensure_ascii=False, indent=1)
