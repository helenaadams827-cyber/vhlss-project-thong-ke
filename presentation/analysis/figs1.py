# -*- coding: utf-8 -*-
"""Hình cho Mục 1–3 và Bước 1–3."""
import json, numpy as np, pandas as pd
from style import *

df = pd.read_csv(ROOT + "/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy()
N = {}
SC = {"Toàn quốc": df.area > 0, "Thành thị": df.area == 1, "Nông thôn": df.area == 2,
      "T1": df.tier == "T1", "T2": df.tier == "T2", "T3": df.tier == "T3", "T4": df.tier == "T4"}
def sc(dd, name): return dd[SC[name].reindex(dd.index)]
def share(g, col): return g[col].sum() / g.tot.sum() * 100
Q = [1, 2, 3, 4]; QL = ["Q1", "Q2", "Q3", "Q4"]; AREAS = ["Thành thị", "Nông thôn"]; TIERS = ["T1", "T2", "T3", "T4"]

# ---------------- Mục 1: mẫu
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.6]})
cnt = df.area_l.value_counts()[AREAS]
w, _ = a.pie(cnt.values, colors=[BLUE, ORANGE], startangle=90, counterclock=False, wedgeprops={"edgecolor": SURF, "linewidth": 2, "width": 0.45})
for wedge, lab, v in zip(w, AREAS, cnt.values):
    ang = np.deg2rad((wedge.theta1 + wedge.theta2) / 2); a.text(1.1 * np.cos(ang), 1.1 * np.sin(ang), f"{lab}\n{vn(v / cnt.sum() * 100, 1)}%", ha="left" if np.cos(ang) > 0 else "right", va="center", fontsize=7, color=INK2)
a.set_title("Cơ cấu mẫu (gộp 3 năm)"); a.set_aspect("equal")
ct = df.groupby(["Year", "area_l"]).size().unstack()[AREAS]
x = np.arange(3)
for i, ar in enumerate(AREAS):
    r = bars(b, x + (i - 0.5) * 0.36, ct[ar].values, AREA[ar], width=0.34, label=ar)
    label_bars(b, r, lambda v: vn(v), dy=60, size=6)
b.set_xticks(x, ["2010", "2012", "2014"]); b.yaxis.set_major_formatter(num_fmt()); b.set_title("Số hộ theo năm và khu vực"); b.legend(loc="upper left", ncols=2, bbox_to_anchor=(0, 1.02))
b.set_ylim(0, 9000)
plt.subplots_adjust(wspace=0.55); save(fig, "f01_sample")
N["urban_share"] = {int(y): round((df[df.Year == y].area == 1).mean() * 100, 1) for y in [2010, 2012, 2014]}

# ---------------- Mục 1: phân phối thu nhập
x14 = df[df.Year == 2014].Inc_head
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0))
cap = x14.quantile(0.99)
a.hist(x14[x14 <= cap] / 1000, bins=50, color=BLUE, edgecolor=SURF, linewidth=0.4, zorder=3)
for v, lab, off in [(x14.median() / 1000, "median", -1), (x14.mean() / 1000, "mean", 1)]:
    a.axvline(v, color=INK2, lw=1, zorder=4); a.text(v + off * 1.5, a.get_ylim()[1] * 0.92, f"{lab} {vn(v, 1)}", ha="left" if off > 0 else "right", fontsize=6.5, color=INK2)
a.set_title("Thang gốc (bỏ 1% cao nhất để vẽ)"); a.set_xlabel("Inc_head 2014, triệu đồng/người/năm"); a.yaxis.set_major_formatter(num_fmt())
lg = np.log10(x14)
b.hist(lg, bins=50, color=BLUE, edgecolor=SURF, linewidth=0.4, zorder=3)
b.set_title("Thang log: gần đối xứng"); b.set_xlabel("log10(Inc_head)"); b.yaxis.set_major_formatter(num_fmt())
ticks = [3, 3.5, 4, 4.5, 5, 5.5, 6]; b.set_xticks(ticks, ["1", "3,2", "10", "32", "100", "316", "1.000"]); b.set_xlabel("Inc_head 2014, triệu đồng (thang log)")
save(fig, "f02_income")
allx = df.Inc_head
N["inc"] = dict(mean=round(allx.mean()), median=round(allx.median()), skew=round(allx.skew(), 1), mean14=round(x14.mean()), med14=round(x14.median()),
               out=round(((allx > allx.quantile(.75) + 1.5 * (allx.quantile(.75) - allx.quantile(.25))).mean()) * 100, 1), max=round(allx.max()))

# ---------------- Mục 2: fuel
st = df.assign(s=np.select([df.fuel_na, df.fuel == 0], ["trống", "0"], ">0"))
tab = pd.crosstab([st.Year, st.area_l], st.s, normalize="index") * 100
fig, a = plt.subplots(figsize=(3.75, 2.35))
labels = []; xs = []
k = 0
for y in [2010, 2012, 2014]:
    for ar in AREAS:
        z = tab.loc[(y, ar)]; b0 = z.get("0", 0); bn = z.get("trống", 0)
        a.bar(k, b0, width=0.6, color=AQUA, edgecolor=SURF, linewidth=1.2, zorder=3, label="Ghi 0" if k == 0 else None)
        a.bar(k, bn, bottom=b0, width=0.6, color=ORANGE, edgecolor=SURF, linewidth=1.2, zorder=3, label="Ô trống" if k == 0 else None)
        a.text(k, b0 + bn + 0.2, vn(b0 + bn, 1) + "%", ha="center", va="bottom", fontsize=6, color=INK2)
        labels.append(f"{y}\n{'TT' if ar == 'Thành thị' else 'NT'}"); xs.append(k); k += 1
    k += 0.5
a.set_xticks(xs, labels); a.yaxis.set_major_formatter(pct_fmt()); a.set_title("% hộ không có chi nhiên liệu dương"); a.legend(loc="upper left")
a.set_ylim(0, 12.5)
save(fig, "f03_fuel")
d14 = df[df.Year == 2014]
N["fuel"] = dict(na14_rural=round(d14[d14.area == 2].fuel_na.mean() * 100, 1), na14_urban=round(d14[d14.area == 1].fuel_na.mean() * 100, 1),
                 na14_q1=round(d14[d14.Quart == 1].fuel_na.mean() * 100, 1), na14_q4=round(d14[d14.Quart == 4].fuel_na.mean() * 100, 1),
                 zeros={int(y): int(((df.Year == y) & (df.fuel == 0) & ~df.fuel_na).sum()) for y in [2010, 2012, 2014]})

# ---------------- Mục 2: vì sao điền 0 — không xóa dòng, không thay median/mean
A9 = ["oto", "moto", "bicycle", "bed", "tab", "tele", "tv", "emachine", "hmachine"]
obs14 = d14.loc[~d14.fuel_na, "fuel"]                     # nhiên liệu 2014 của các hộ có khai
q1f = d14[d14.Quart == 1]
way = {"Điền 0": q1f.fuel.mean(),                          # cách đang dùng
       "Xóa dòng thiếu": q1f.loc[~q1f.fuel_na, "fuel"].mean(),
       "Điền median": q1f.fuel.where(~q1f.fuel_na, obs14.median()).mean(),
       "Điền mean": q1f.fuel.where(~q1f.fuel_na, obs14.mean()).mean()}
ana = df.asset_na.astype(bool)
rec = df[~ana & df[A9].notna().all(axis=1)]                # hộ có đủ 9 cột tài sản
kq1 = (rec.loc[rec.Quart == 1, A9] > 0).sum(axis=1)        # số món hộ Q1 có
OWN = {"TV": "tv", "Điện thoại": "tele", "Xe máy": "moto"}
def gap(c, keep): return ((df[keep & (df.Quart == 4)][c] > 0).mean() - (df[keep & (df.Quart == 1)][c] > 0).mean()) * 100
allrows = df.Quart > 0
gaps = {l: (gap(c, allrows), gap(c, ~ana)) for l, c in OWN.items()}

fig, (a, b) = plt.subplots(2, 1, figsize=(3.3, 3.25), gridspec_kw={"height_ratios": [1.15, 1], "hspace": 0.75})
names = list(way)[::-1]; vals = [way[n] / 1000 for n in names]
r = a.barh(np.arange(4), vals, height=0.6, color=[CORAL, CORAL, CORAL, AQUA], edgecolor=SURF, linewidth=1, zorder=3)
for i, (n, v) in enumerate(zip(names, vals)):
    extra = "" if n == "Điền 0" else f"  (+{vn((way[n] / way['Điền 0'] - 1) * 100)}%)"
    a.text(v + 0.05, i, vn(v, 2) + extra, va="center", fontsize=6.3, color=INK2)
a.set_yticks(np.arange(4), names); a.set_xlim(0, 4.6); a.xaxis.set_major_formatter(num_fmt(1))
a.set_title("Nhiên liệu TB của hộ Q1 năm 2014 (triệu đồng)")
y = np.arange(len(OWN)); h = 0.36
r0 = b.barh(y - h / 2, [gaps[l][0] for l in OWN], height=h, color=AQUA, edgecolor=SURF, linewidth=1, zorder=3, label="Điền 0")
r1 = b.barh(y + h / 2, [gaps[l][1] for l in OWN], height=h, color=CORAL, edgecolor=SURF, linewidth=1, zorder=3, label="Xóa 284 hộ")
for rr in (r0, r1):
    for rect in rr: b.text(rect.get_width() + 0.4, rect.get_y() + rect.get_height() / 2, vn(rect.get_width(), 1), va="center", fontsize=6.1, color=INK2)
b.set_yticks(y, list(OWN)); b.invert_yaxis(); b.set_xlim(0, 44)
b.set_title("Khoảng cách sở hữu Q4 – Q1 (điểm %)")
b.legend(loc="upper right", ncols=2, fontsize=6, handlelength=1, columnspacing=0.8, borderaxespad=0.2)
save(fig, "f03b_missing")
N["missing"] = dict(
    fuel_q1_2014={k: round(v) for k, v in way.items()},
    fuel_q1_2014_vs0={k: round((v / way["Điền 0"] - 1) * 100) for k, v in way.items()},
    fuel14_mean=round(obs14.mean()), fuel14_median=round(obs14.median()),
    fuel14_q1_reporter_median=round(q1f.loc[~q1f.fuel_na, "fuel"].median()),
    sd14_obs=round(obs14.std()), sd14_meanfill=round(d14.fuel.where(~d14.fuel_na, obs14.mean()).std()),
    sd14_change=round((d14.fuel.where(~d14.fuel_na, obs14.mean()).std() / obs14.std() - 1) * 100, 1),
    asset_allzero=int(((rec[A9] > 0).sum(axis=1) == 0).sum()), asset_blank=int(ana.sum()),
    q1_items={int(i): round((kq1 == i).mean() * 100, 1) for i in range(4)},
    asset_blank_q1=round(ana[df.Quart == 1].mean() * 100, 1), asset_blank_q4=round(ana[df.Quart == 4].mean() * 100, 1),
    asset_blank_noelec=round((df.loc[ana, "elec"] == 0).mean() * 100),
    q1_noelec=round((df.loc[~ana & (df.Quart == 1), "elec"] == 0).mean() * 100),
    gap={l: [round(g0, 1), round(g1, 1)] for l, (g0, g1) in gaps.items()},
    fhouse_zero=round((df.fhouse == 0).mean() * 100), house_na=int(df.house.isna().sum()))

# ---------------- Mục 3: nhóm tỉnh
pm = df[df.Year == 2014].groupby("province").agg(med=("Inc_head", "median"), tier=("tier", "first"), name=("province_name", "first")).sort_values("med")
fig, a = plt.subplots(figsize=(5.9, 2.25))
cols = [ORD4[TIERS.index(t)] for t in pm.tier]
a.bar(np.arange(len(pm)), pm.med / 1000, width=0.72, color=cols, edgecolor=SURF, linewidth=0.5, zorder=3)
a.set_xticks(np.arange(len(pm)), pm.name, rotation=90, fontsize=4.8); a.set_xlim(-0.8, len(pm) - 0.2)
a.set_ylabel("Median Inc_head 2014\n(triệu đồng/người/năm)", fontsize=6.5); a.yaxis.set_major_formatter(num_fmt())
from matplotlib.patches import Patch
a.legend(handles=[Patch(color=c, label=t) for c, t in zip(ORD4, ["T1 (nghèo nhất)", "T2", "T3", "T4 (giàu nhất)"])], loc="upper left", ncols=4)
save(fig, "f04_tiers")

# ---------------- A1
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.05), gridspec_kw={"width_ratios": [1, 1.25]})
data = [x14[df[df.Year == 2014].Quart == q] / 1000 for q in Q]
bp = a.boxplot(data, widths=0.5, patch_artist=True, showfliers=True, flierprops=dict(marker="o", ms=1.5, mfc=MUTED, mec="none", alpha=0.4), medianprops=dict(color=SURF, lw=1.5), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED))
for p, c in zip(bp["boxes"], ORD4): p.set_facecolor(c); p.set_edgecolor(c)
a.set_yscale("log"); a.set_xticks([1, 2, 3, 4], QL); a.set_title("Inc_head 2014 theo Q (thang log)")
a.yaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(v, 0) if v >= 1 else vn(v, 1))); a.set_ylabel("triệu đồng/người/năm", fontsize=6.5)
ratio = {}; q91 = {}
for name in SC:
    g = df[(df.Year == 2014) & SC[name]]
    m = g.groupby("Quart").Inc_head.median(); ratio[name] = m[4] / m[1]; q91[name] = g.Inc_head.quantile(.9) / g.Inc_head.quantile(.1)
r = bars(b, np.arange(7), list(ratio.values()), [GRAY] * 3 + ORD4, width=0.6)
label_bars(b, r, lambda v: vn(v, 1) + " lần", dy=0.08, size=6.2)
b.set_xticks(np.arange(7), ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"], fontsize=6); b.set_title("Median Q4 / median Q1 (2014)"); b.set_ylim(0, 7.3)
plt.subplots_adjust(wspace=0.35)
save(fig, "f05_A1")
g14 = df[df.Year == 2014]
N["A1"] = dict(ratio={k: round(v, 2) for k, v in ratio.items()}, q91={k: round(v, 1) for k, v in q91.items()},
               medQ=g14.groupby("Quart").Inc_head.median().round().to_dict(), meanQ=g14.groupby("Quart").Inc_head.mean().round().to_dict(),
               q10=round(g14.Inc_head.quantile(.1)), q90=round(g14.Inc_head.quantile(.9)))

# ---------------- A2
names = ["Thành thị", "Nông thôn", "T1", "T2", "T3", "T4"]
comp = pd.DataFrame({n: df[SC[n]].Quart.value_counts(normalize=True).sort_index() * 100 for n in names}).T
fig, a = plt.subplots(figsize=(3.75, 2.45))
bottom = np.zeros(len(names))
for qi, q in enumerate(Q):
    v = comp[q].values
    a.bar(np.arange(len(names)), v, bottom=bottom, width=0.62, color=ORD4[qi], edgecolor=SURF, linewidth=1.2, zorder=3, label=QL[qi])
    for i, (vv, bb) in enumerate(zip(v, bottom)):
        if vv >= 8: a.text(i, bb + vv / 2, vn(vv) + "%", ha="center", va="center", fontsize=6, color=INK if qi < 2 else "white")
    bottom += v
a.set_xticks(np.arange(len(names)), ["Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"]); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 100)
a.legend(loc="upper center", ncols=4, bbox_to_anchor=(0.5, 1.13)); a.grid(False)
save(fig, "f06_A2")
N["A2"] = comp.round(0).to_dict("index")

# ---------------- A3
cv = {}
for n in SC:
    for y in [2010, 2012, 2014]:
        s = df[SC[n] & (df.Year == y)].Inc_head; t = s[s <= s.quantile(.99)]
        cv[(n, y)] = dict(raw=s.std() / s.mean(), trim=t.std() / t.mean(), iqrm=(s.quantile(.75) - s.quantile(.25)) / s.median(), sd=s.std(), rng=s.max() - s.min())
fig, a = plt.subplots(figsize=(3.75, 2.35))
xs = np.arange(7)
for i, y in enumerate([2010, 2012, 2014]):
    bars(a, xs + (i - 1) * 0.26, [cv[(n, y)]["trim"] for n in SC], ORD3[i], width=0.25, label=str(y))
a.set_xticks(xs, ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"], fontsize=6); a.yaxis.set_major_formatter(num_fmt(1)); a.set_ylim(0, 0.95)
a.set_title("CV của Inc_head (đã bỏ 1% hộ cao nhất)"); a.legend(loc="upper right", ncols=3)
save(fig, "f07_A3")
N["A3"] = {f"{n}|{y}": {k: round(v, 3) for k, v in dd.items()} for (n, y), dd in cv.items()}

# ---------------- B1
fig, a = plt.subplots(figsize=(3.0, 2.35))
nec = [share(d[d.Quart == q], "nec") for q in Q]
a.bar(np.arange(4), nec, width=0.6, color=BLUE, edgecolor=SURF, linewidth=1.2, zorder=3, label="Thiết yếu")
a.bar(np.arange(4), [100 - v for v in nec], bottom=nec, width=0.6, color=ORANGE, edgecolor=SURF, linewidth=1.2, zorder=3, label="Không thiết yếu")
for i, v in enumerate(nec):
    a.text(i, v / 2, vn(v, 1) + "%", ha="center", va="center", color=INK, fontsize=6.5)
    a.text(i, v + (100 - v) / 2, vn(100 - v, 1) + "%", ha="center", va="center", color=INK, fontsize=6.5)
a.set_xticks(np.arange(4), QL); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 100); a.grid(False)
a.legend(loc="upper center", ncols=2, bbox_to_anchor=(0.5, 1.12))
save(fig, "f08_B1a")
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 1.95), sharey=True)
for ar in AREAS:
    v = [share(d[(d.Quart == q) & (d.area_l == ar)], "nec") for q in Q]
    a.plot(np.arange(4), v, color=AREA[ar], marker="o", ms=5, mec=SURF, mew=1.2, label=ar)
a.set_title("Thành thị và nông thôn"); a.legend(loc="lower left")
for ti, t in enumerate(TIERS):
    v = [share(d[(d.Quart == q) & (d.tier == t)], "nec") for q in Q]
    b.plot(np.arange(4), v, color=ORD4[ti], marker="o", ms=5, mec=SURF, mew=1.2, label=t)
b.set_title("4 nhóm tỉnh"); b.legend(loc="lower left", ncols=4)
for ax in (a, b):
    ax.set_xticks(np.arange(4), QL); ax.yaxis.set_major_formatter(pct_fmt()); ax.set_ylim(62, 80)
a.set_ylabel("% chi cho thiết yếu", fontsize=6.5)
save(fig, "f09_B1b")
N["B1"] = dict(nat=[round(v, 1) for v in nec], area={ar: [round(share(d[(d.Quart == q) & (d.area_l == ar)], "nec"), 1) for q in Q] for ar in AREAS},
               tier={t: [round(share(d[(d.Quart == q) & (d.tier == t)], "nec"), 1) for q in Q] for t in TIERS},
               mean_hh=[round((d[d.Quart == q].nec / d[d.Quart == q].tot).mean() * 100, 1) for q in Q],
               med_hh=[round((d[d.Quart == q].nec / d[d.Quart == q].tot).median() * 100, 1) for q in Q])

# ---------------- B2
e14 = d[d.Year == 2014]
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.3]})
qs = e14.groupby("Quart").burden.quantile([.25, .5, .75]).unstack() * 100
r = bars(a, np.arange(4), qs[0.5].values, ORD4, width=0.55)
a.vlines(np.arange(4), qs[0.25], qs[0.75], color=INK2, lw=1, zorder=4)
for i in range(4): a.text(i + 0.33, qs.loc[i + 1, 0.5], vn(qs.loc[i + 1, 0.5], 1) + "%", va="center", fontsize=6.2, color=INK2)
a.set_xticks(np.arange(4), QL); a.yaxis.set_major_formatter(pct_fmt()); a.set_title("Chi thiết yếu / thu nhập (2014)\ncột = median, vạch = Q1–Q3")
q1b = {n: sc(e14, n)[sc(e14, n).Quart == 1].burden.median() * 100 for n in SC}
r = bars(b, np.arange(7), list(q1b.values()), [GRAY] * 3 + ORD4, width=0.6)
label_bars(b, r, lambda v: vn(v, 0) + "%", dy=1.5, size=6.2)
b.set_xticks(np.arange(7), ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"], fontsize=6); b.yaxis.set_major_formatter(pct_fmt()); b.set_title("Riêng hộ Q1: median chi thiết yếu / thu nhập"); b.set_ylim(0, 105)
a.set_xlim(-0.55, 4.0); plt.subplots_adjust(wspace=0.3)
save(fig, "f10_B2")
N["B2"] = dict(q=qs.round(1).to_dict("index"), mean=[round(e14[e14.Quart == q].burden.mean() * 100, 1) for q in Q], q1=dict((k, round(v, 1)) for k, v in q1b.items()))

# ---------------- B4 pies
NAME = {"rice": "gạo", "nrice": "TP khác", "fuel": "nhiên liệu", "med": "thuốc, viện phí", "nfood": "ngoài ăn uống", "edu": "giáo dục", "tobaco": "thuốc lá", "other": "khác"}
NEC = ["rice", "nrice", "water", "elec", "fuel", "garb", "med", "hins", "aid", "fhouse"]
NECC = [BLUE, AMBER, TEAL, ROSE, LIGHTGRAY]; UNNC = [LAVENDER, CORAL, SLATE]
def within(g, items, den): return g[items].sum() / g[den].sum() * 100
fig, axes = plt.subplots(2, 5, figsize=(5.9, 2.5), gridspec_kw={"width_ratios": [1, 1, 1, 1, 1.25]})
pieN = {}
for qi, q in enumerate(Q):
    g = d[d.Quart == q]
    wn = within(g, NEC, "nec"); main = wn[["nrice", "rice", "fuel", "med"]]; vals = list(main.values) + [100 - main.sum()]
    labs = ["TP khác", "gạo", "nhiên liệu", "thuốc, viện phí", "khác"]
    wu = within(g, ["nfood", "edu", "tobaco"], "unn")
    pieN[q] = dict(nec=dict(zip(labs, [round(v, 1) for v in vals])), unn={"ngoài ăn uống": round(wu["nfood"], 1), "giáo dục": round(wu["edu"], 1), "thuốc lá": round(wu["tobaco"], 1)})
    for row, (vv, cl) in enumerate([(vals, NECC), (list(wu.values), UNNC)]):
        ax = axes[row, qi]
        ws, _ = ax.pie(vv, colors=cl, startangle=90, counterclock=False, wedgeprops={"edgecolor": SURF, "linewidth": 1.5})
        for wdg, v, c in zip(ws, vv, cl):
            if v < 8: continue
            ang = np.deg2rad((wdg.theta1 + wdg.theta2) / 2); rr = 0.62
            lum = int(c[1:3], 16) * 0.299 + int(c[3:5], 16) * 0.587 + int(c[5:7], 16) * 0.114
            ax.text(rr * np.cos(ang), rr * np.sin(ang), vn(v) + "%", ha="center", va="center", fontsize=6.4, color="white" if lum < 110 else INK)
        ax.set_aspect("equal")
        if row == 0: ax.set_title(QL[qi], loc="center")
axes[0, 0].text(-1.6, 0, "Thiết yếu", rotation=90, va="center", ha="center", fontsize=7, color=INK2, fontweight="bold")
axes[1, 0].text(-1.6, 0, "Không\nthiết yếu", rotation=90, va="center", ha="center", fontsize=7, color=INK2, fontweight="bold")
for row in (0, 1): axes[row, 4].axis("off")
axes[0, 4].legend(handles=[Patch(color=c, label=l) for c, l in zip(NECC, ["TP khác", "gạo", "nhiên liệu", "thuốc, viện phí", "khác (điện, nước,\nrác, BHYT, nhà…)"])], loc="center left", fontsize=6.6, frameon=False, handlelength=1.0)
axes[1, 4].legend(handles=[Patch(color=c, label=l) for c, l in zip(UNNC, ["ngoài ăn uống", "giáo dục", "thuốc lá"])], loc="center left", fontsize=6.6, frameon=False, handlelength=1.0)
plt.subplots_adjust(wspace=0.05, hspace=0.12)
save(fig, "f11_B4pies")
N["B4pies"] = pieN

# ---------------- B4 top 3
F13 = ["rice", "nrice", "tobaco", "nfood", "edu", "med", "hins", "aid", "water", "elec", "garb", "fuel", "fhouse"]
ITEMC = {"nrice": BLUE, "nfood": LAVENDER, "rice": AMBER, "fuel": TEAL, "med": ROSE, "edu": CORAL}
fig, axes = plt.subplots(1, 4, figsize=(5.9, 1.6), sharex=True)
top = {}
for qi, q in enumerate(Q):
    g = d[d.Quart == q]; s = (g[F13].sum() / g.tot.sum() * 100).sort_values(ascending=False).head(3)
    top[q] = {NAME.get(k, k): round(v, 1) for k, v in s.items()}
    ax = axes[qi]; y = np.arange(3)[::-1]
    r = hbars(ax, y, s.values, [ITEMC[k] for k in s.index], height=0.55)
    for yy, k, v in zip(y, s.index, s.values):
        ax.text(v + 1.5, yy, f"{NAME[k]} {vn(v, 1)}%", va="center", fontsize=5.8, color=INK2)
    ax.set_yticks([]); ax.set_title(QL[qi], loc="left"); ax.set_xlim(0, 100); ax.grid(False); ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
save(fig, "f12_B4top")
N["B4top"] = top

# ---------------- C1
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.2]})
rice = [share(d[d.Quart == q], "rice") for q in Q]; nr = [share(d[d.Quart == q], "nrice") for q in Q]
rest = [100 - r1 - r2 for r1, r2 in zip(rice, nr)]
bt = np.zeros(4)
for vals, c, l in [(rice, AMBER, "gạo"), (nr, BLUE, "thực phẩm khác"), (rest, LIGHTGRAY, "phần còn lại")]:
    a.bar(np.arange(4), vals, bottom=bt, width=0.6, color=c, edgecolor=SURF, linewidth=1.2, zorder=3, label=l)
    for i, (v, b0) in enumerate(zip(vals, bt)):
        if v >= 4 and l != "phần còn lại": a.text(i, b0 + v / 2, vn(v, 1) + "%", ha="center", va="center", fontsize=6, color=INK)
    bt += np.array(vals)
a.set_xticks(np.arange(4), QL); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 100); a.grid(False)
a.legend(loc="upper center", ncols=3, bbox_to_anchor=(0.5, 1.14), fontsize=6.3)
rp = e14.assign(r=e14.rice / e14["size"])
for i, ar in enumerate(AREAS):
    v = [rp[(rp.Quart == q) & (rp.area_l == ar)].r.median() / 1000 for q in Q]
    bars(b, np.arange(4) + (i - 0.5) * 0.36, v, AREA[ar], width=0.34, label=ar)
b.set_xticks(np.arange(4), QL); b.yaxis.set_major_formatter(num_fmt(1)); b.set_title("Median tiền gạo / người, 2014 (triệu đồng)"); b.legend(loc="upper center", ncols=2, bbox_to_anchor=(0.5, 1.0)); b.set_ylim(0, 1.9)
save(fig, "f13_C1")
N["C1"] = dict(food=[round(share(d[d.Quart == q], "food"), 1) for q in Q], rice=[round(v, 1) for v in rice], nrice=[round(v, 1) for v in nr],
               ricepc=[round(rp[rp.Quart == q].r.median()) for q in Q], ricepc_mean=[round(rp[rp.Quart == q].r.mean()) for q in Q],
               ricepc_cv=[round(rp[rp.Quart == q].r.std() / rp[rp.Quart == q].r.mean(), 2) for q in Q])

# ---------------- C2
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.95))
ep = e14.assign(e=e14.elec / e14["size"])
v = [ep[ep.Quart == q].e.median() for q in Q]
r = bars(axs[0], np.arange(4), v, ORD4, width=0.55); label_bars(axs[0], r, lambda z: vn(z), dy=15, size=6)
axs[0].set_title("Median tiền điện / người\n2014 (nghìn đồng)"); axs[0].yaxis.set_major_formatter(num_fmt()); axs[0].set_ylim(0, 1150)
for ax, col, ttl in [(axs[1], "water", "% hộ trả tiền nước"), (axs[2], "garb", "% hộ trả phí rác")]:
    for i, ar in enumerate(AREAS):
        vv = [(d[(d.Quart == q) & (d.area_l == ar)][col] > 0).mean() * 100 for q in Q]
        bars(ax, np.arange(4) + (i - 0.5) * 0.36, vv, AREA[ar], width=0.34, label=ar)
    ax.set_title(ttl + "\n(gộp 3 năm)"); ax.yaxis.set_major_formatter(pct_fmt()); ax.set_ylim(0, 100)
axs[1].legend(loc="upper left", fontsize=6)
for ax in axs: ax.set_xticks(np.arange(4), QL)
plt.subplots_adjust(wspace=0.45); save(fig, "f14_C2")
N["C2"] = dict(elec=[round(z) for z in v], elec_mean=[round(ep[ep.Quart == q].e.mean()) for q in Q],
               water={ar: [round((d[(d.Quart == q) & (d.area_l == ar)].water > 0).mean() * 100) for q in Q] for ar in AREAS},
               garb={ar: [round((d[(d.Quart == q) & (d.area_l == ar)].garb > 0).mean() * 100) for q in Q] for ar in AREAS})

# ---------------- C3
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 1.9), sharey=True)
for ax, col, ttl in [(a, "health", "Y tế / tổng chi"), (b, "edu", "Giáo dục / tổng chi")]:
    for i, ar in enumerate(AREAS):
        vv = [share(d[(d.Quart == q) & (d.area_l == ar)], col) for q in Q]
        r = bars(ax, np.arange(4) + (i - 0.5) * 0.36, vv, AREA[ar], width=0.34, label=ar)
        label_bars(ax, r, lambda z: vn(z, 1), dy=0.1, size=5.8)
    ax.set_title(ttl); ax.set_xticks(np.arange(4), QL); ax.yaxis.set_major_formatter(pct_fmt())
a.set_ylim(0, 9.5); a.legend(loc="upper left", ncols=2)
plt.subplots_adjust(wspace=0.12); save(fig, "f15_C3")
N["C3"] = dict(health={ar: [round(share(d[(d.Quart == q) & (d.area_l == ar)], "health"), 1) for q in Q] for ar in AREAS},
               edu={ar: [round(share(d[(d.Quart == q) & (d.area_l == ar)], "edu"), 1) for q in Q] for ar in AREAS},
               edu_nat=[round(share(d[d.Quart == q], "edu"), 1) for q in Q], edu_p=[round((d[d.Quart == q].edu > 0).mean() * 100) for q in Q],
               health_tier_q1={t: round(share(d[(d.Quart == 1) & (d.tier == t)], "health"), 1) for t in TIERS})

# ---------------- C4
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.9))
v = [share(d[d.Quart == q], "nfood") for q in Q]
r = bars(axs[0], np.arange(4), v, ORD4, width=0.55); label_bars(axs[0], r, lambda z: vn(z, 1) + "%", dy=0.4, size=6)
axs[0].set_title("Ngoài ăn uống / tổng chi"); axs[0].set_ylim(0, 30); axs[0].yaxis.set_major_formatter(pct_fmt())
for i, ar in enumerate(AREAS):
    vv = [share(d[(d.Quart == q) & (d.area_l == ar)], "tobaco") for q in Q]
    bars(axs[1], np.arange(4) + (i - 0.5) * 0.36, vv, AREA[ar], width=0.34, label=ar)
axs[1].set_title("Thuốc lá / tổng chi"); axs[1].yaxis.set_major_formatter(pct_fmt(1)); axs[1].legend(loc="upper right", fontsize=6); axs[1].set_ylim(0, 1.8)
vt = [share(d[d.tier == t], "tobaco") for t in TIERS]
r = bars(axs[2], np.arange(4), vt, ORD4, width=0.55); label_bars(axs[2], r, lambda z: vn(z, 1) + "%", dy=0.03, size=6)
axs[2].set_title("Thuốc lá theo nhóm tỉnh"); axs[2].set_xticks(np.arange(4), TIERS); axs[2].yaxis.set_major_formatter(pct_fmt(1)); axs[2].set_ylim(0, 1.8)
for ax in axs[:2]: ax.set_xticks(np.arange(4), QL)
plt.subplots_adjust(wspace=0.5); save(fig, "f16_C4")
N["C4"] = dict(nfood=[round(z, 1) for z in v], tob={ar: [round(share(d[(d.Quart == q) & (d.area_l == ar)], "tobaco"), 2) for q in Q] for ar in AREAS},
               tob_nat=[round(share(d[d.Quart == q], "tobaco"), 2) for q in Q], tob_tier=[round(z, 2) for z in vt],
               tob_p={ar: [round((d[(d.Quart == q) & (d.area_l == ar)].tobaco > 0).mean() * 100) for q in Q] for ar in AREAS})

json.dump(N, open(ROOT + "/presentation/analysis/numbers1.json", "w"), ensure_ascii=False, indent=1, default=float)
print(json.dumps(N, ensure_ascii=False, default=float)[:6000])
