# -*- coding: utf-8 -*-
"""Hình cho bài thuyết trình 20 phút (slides_20min.tex) -> figs/g*.pdf, numbers20.json
   Chạy: /home/trang/STATS/.venv/bin/python analysis/figs20.py   (CHECK=1 để dò chữ đè nhau)"""
import json, numpy as np, pandas as pd, matplotlib.pyplot as plt
from style import *   # noqa

df = pd.read_csv(f"{ROOT}/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy()
d["ov"] = d.tot > d.income
d["pc"] = d.tot / d["size"]
Y = [2010, 2012, 2014]; QS = [1, 2, 3, 4]; TS = ["T1", "T2", "T3", "T4"]
M = 1000.0            # nghìn đồng -> triệu đồng
N = {}                # số liệu xuất ra numbers20.json

def med(g, c): return g[c].median()

# =====================================================================  1. THU NHẬP
# ---- g01: dạng phân phối -> dùng median hay mean?
g14 = df[df.Year == 2014]
fig, ax = plt.subplots(1, 3, figsize=(8.16, 1.7))
x = (g14.Inc_head / M).clip(upper=150)
ax[0].hist(x, bins=50, color="#bfd2f3", edgecolor=SURF, linewidth=0.5, zorder=3)
mn, md = g14.Inc_head.mean() / M, g14.Inc_head.median() / M
ax[0].axvline(md, color=TEAL, lw=1.6, zorder=4, label=f"median {vn(md,1)} triệu")
ax[0].axvline(mn, color=CORAL, lw=1.6, zorder=4, label=f"mean {vn(mn,1)} triệu")
ax[0].legend(loc="upper right", fontsize=6.8)
ax[0].set_title("a) Histogram · thu nhập/người 2014", fontsize=7.6)
ax[0].set_xlabel("triệu đồng/người/năm (cắt ở 150)"); ax[0].set_ylabel("số hộ")
ax[0].yaxis.set_major_formatter(num_fmt())

bx = [(g14[g14.Quart == q].Inc_head / M).values for q in QS]
bp = ax[1].boxplot(bx, whis=(5, 95), showfliers=False, patch_artist=True, widths=0.55, zorder=3,
                   medianprops=dict(color=INK, lw=1.4), whiskerprops=dict(color=BASE, lw=1),
                   capprops=dict(color=BASE, lw=1), boxprops=dict(edgecolor=SURF, lw=1))
for p, c in zip(bp["boxes"], ORD4): p.set_facecolor(c)
ax[1].set_xticklabels([f"Q{q}" for q in QS]); ax[1].set_ylabel("triệu đồng/người/năm")
ax[1].set_title("b) Boxplot · hộp 25–75%, râu 5–95%", fontsize=7.6)
ax[1].yaxis.set_major_formatter(num_fmt())
mx = g14[g14.Quart == 4].Inc_head.max() / M
ax[1].annotate(f"Q4 có hộ tới {vn(mx,0)} triệu\n(≈ {vn(mx/(g14[g14.Quart==4].Inc_head.median()/M),0)} lần median Q4)",
               xy=(4, ax[1].get_ylim()[1] * 0.97), xytext=(2.35, ax[1].get_ylim()[1] * 0.80),
               fontsize=6.4, color=INK2, arrowprops=dict(arrowstyle="-", color=BASE, lw=0.8))

w = 0.36; xs = np.arange(4)
mns = [g14[g14.Quart == q].Inc_head.mean() / M for q in QS]
mds = [g14[g14.Quart == q].Inc_head.median() / M for q in QS]
r1 = ax[2].bar(xs - w/2, mds, w, color=TEAL, edgecolor=SURF, lw=1.2, zorder=3, label="median")
r2 = ax[2].bar(xs + w/2, mns, w, color=CORAL, edgecolor=SURF, lw=1.2, zorder=3, label="mean")
for rr, cc in ((r1[3], TEAL), (r2[3], CORAL)):
    ax[2].text(rr.get_x() + rr.get_width()/2, rr.get_height() + 0.8, vn(rr.get_height(), 1), ha="center", fontsize=6.4, color=cc)
ax[2].text(0.03, 0.62, "Q1–Q3: mean ≈ median", transform=ax[2].transAxes, fontsize=6.2, color=INK2)
ax[2].set_xticks(xs); ax[2].set_xticklabels([f"Q{q}" for q in QS]); ax[2].legend(loc="upper left")
ax[2].set_title("c) Bar · mean so với median", fontsize=7.6)
ax[2].set_ylabel("triệu đồng/người/năm"); ax[2].set_ylim(0, max(mns) * 1.22)
ax[2].yaxis.set_major_formatter(num_fmt())
for a in ax: a.tick_params(labelsize=6.8)
save(fig, "g01_shape")
N["shape"] = {f"Q{q}": dict(mean=round(g14[g14.Quart == q].Inc_head.mean()/M, 2), median=round(g14[g14.Quart == q].Inc_head.median()/M, 2),
                            skew=round(g14[g14.Quart == q].Inc_head.skew(), 2),
                            below=round((g14[g14.Quart == q].Inc_head < g14[g14.Quart == q].Inc_head.mean()).mean()*100, 1)) for q in QS}
N["ratio_median"] = round(mds[3]/mds[0], 2); N["ratio_mean"] = round(mns[3]/mns[0], 2)

# ---- g02: thu nhập median theo Q qua 3 năm + khoảng cách
fig, ax = plt.subplots(1, 2, figsize=(8.16, 1.7), gridspec_kw=dict(width_ratios=[1.25, 1]))
tab = {q: [df[(df.Year == y) & (df.Quart == q)].Inc_head.median()/M for y in Y] for q in QS}
for q, c in zip(QS, ORD4):
    ax[0].plot(Y, tab[q], "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[0].text(2014.15, tab[q][2], f"Q{q}  {vn(tab[q][2],1)}", color=c if q > 1 else "#6380c8", fontsize=7, va="center")
    ax[0].text(2009.85, tab[q][0], vn(tab[q][0], 1), color=INK2, fontsize=6.5, va="center", ha="right")
ax[0].set_xticks(Y); ax[0].set_xlim(2009.2, 2015.4); ax[0].set_ylabel("triệu đồng/người/năm")
ax[0].set_title("a) Line chart · median thu nhập/người", fontsize=7.6)
ax[0].yaxis.set_major_formatter(num_fmt())
gap = [tab[4][i] - tab[1][i] for i in range(3)]; rat = [tab[4][i]/tab[1][i] for i in range(3)]
r = bars(ax[1], np.arange(3), gap, "#8dabe4", width=0.52)
label_bars(ax[1], r, lambda v: vn(v, 1) + " tr", dy=0.8, size=7)
ax[1].set_xticks(np.arange(3)); ax[1].set_xticklabels(Y)
ax[1].set_ylabel("khoảng cách tuyệt đối Q4 − Q1 (triệu)"); ax[1].set_ylim(0, max(gap)*1.3)
ax[1].yaxis.set_major_formatter(num_fmt())
for i, v in enumerate(rat):
    ax[1].text(i, gap[i]/2, f"gấp {vn(v,2)} lần", ha="center", va="center", fontsize=7, color="white")
ax[1].set_title("b) Bar · khoảng cách Q4 − Q1", fontsize=7.6)
for a in ax: a.tick_params(labelsize=6.8)
save(fig, "g02_inc_line")
N["inc_q"] = {f"Q{q}": [round(v, 2) for v in tab[q]] for q in QS}
N["inc_growth"] = {f"Q{q}": round((tab[q][2]/tab[q][0] - 1)*100) for q in QS}
N["gap"] = [round(g, 1) for g in gap]; N["gap_ratio"] = [round(v, 2) for v in rat]

# ---- g03: pie — 100 người và 100 đồng thu nhập chia thế nào?
fig = plt.figure(figsize=(8.16, 1.7))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.15], wspace=0.42)
a0, a1, a2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
pop = [g14[g14.Quart == q]["size"].sum() / g14["size"].sum() * 100 for q in QS]
inc = [g14[g14.Quart == q].income.sum() / g14.income.sum() * 100 for q in QS]
for a, vals, ttl in [(a0, pop, "a) Pie chart · 100 người dân"),
                     (a1, inc, "b) Pie chart · 100 đồng thu nhập")]:
    a.pie(vals, labels=[f"Q{q}\n{vn(v,1)}%" for q, v in zip(QS, vals)], colors=ORD4,
          startangle=90, counterclock=False, labeldistance=1.16, radius=0.88,
          wedgeprops=dict(edgecolor=SURF, linewidth=1.6), textprops=dict(fontsize=7.2, color=INK2))
    a.set_title(ttl, fontsize=7.6, loc="center")
bottom = np.zeros(3)
for i, (q, c) in enumerate(zip(QS, ORD4)):
    sh = [df[(df.Year == y) & (df.Quart == q)].income.sum() / df[df.Year == y].income.sum() * 100 for y in Y]
    r = a2.barh(np.arange(3), sh, left=bottom, height=0.5, color=c, edgecolor=SURF, lw=1.4, zorder=3)
    for j, v in enumerate(sh):
        a2.text(bottom[j] + v/2, j, vn(v, 1), ha="center", va="center", fontsize=6.6,
                color="white" if i >= 2 else INK2)
    bottom += np.array(sh)
a2.set_yticks(np.arange(3)); a2.set_yticklabels(Y); a2.set_xlim(0, 100); a2.set_xticks([])
a2.grid(False); a2.set_title("c) Stacked bar · 3 năm (%)", fontsize=7.6)
for s in a2.spines.values(): s.set_visible(False)
a2.tick_params(labelsize=7)
save(fig, "g03_pie")
N["pie"] = dict(pop=[round(v, 1) for v in pop], inc=[round(v, 1) for v in inc],
                inc2010=[round(df[(df.Year == 2010) & (df.Quart == q)].income.sum()/df[df.Year == 2010].income.sum()*100, 1) for q in QS])

# ---- g04: dumbbell — thành thị/nông thôn và T1–T4, 2010 -> 2014
fig, ax = plt.subplots(1, 2, figsize=(8.16, 1.7), gridspec_kw=dict(width_ratios=[1, 1.12]))
def dumb(a, labels, v10, v14, colors, ttl):
    ys = np.arange(len(labels))[::-1]
    for i, y in enumerate(ys):
        a.plot([v10[i], v14[i]], [y, y], color=GRID, lw=5, solid_capstyle="round", zorder=2)
        a.plot([v10[i]], [y], "o", ms=7, color=BASE, mec=SURF, mew=1.4, zorder=3)
        a.plot([v14[i]], [y], "o", ms=7, color=colors[i], mec=SURF, mew=1.4, zorder=4)
        a.text(v10[i] - 1.2, y, vn(v10[i], 1), ha="right", va="center", fontsize=6.6, color=MUTED)
        a.text(v14[i] + 1.2, y, f"{vn(v14[i],1)}  (+{round((v14[i]/v10[i]-1)*100)}%)", ha="left", va="center", fontsize=6.8, color=INK2)
    a.set_yticks(ys); a.set_yticklabels(labels); a.set_ylim(-0.6, len(labels) - 0.4)
    a.grid(False); a.set_xlabel("median thu nhập/người/năm (triệu đồng)")
    a.set_xlim(0, max(v14) * 1.42); a.set_title(ttl, fontsize=7.6)
    a.xaxis.set_major_formatter(num_fmt())
areas = ["Thành thị", "Nông thôn"]
v10 = [df[(df.Year == 2010) & (df.area == a_)].Inc_head.median()/M for a_ in (1, 2)]
v14 = [df[(df.Year == 2014) & (df.area == a_)].Inc_head.median()/M for a_ in (1, 2)]
dumb(ax[0], areas, v10, v14, [BLUE, CORAL], "a) Dumbbell · thành thị – nông thôn")
t10 = [df[(df.Year == 2010) & (df.tier == t)].Inc_head.median()/M for t in TS]
t14 = [df[(df.Year == 2014) & (df.tier == t)].Inc_head.median()/M for t in TS]
dumb(ax[1], ["T1 (nghèo)", "T2", "T3", "T4 (giàu)"], t10, t14, ORD4,
     "b) Dumbbell · 4 nhóm tỉnh")
ytop = len(TS) - 1
ax[1].annotate("2010", xy=(t10[0], ytop), xytext=(t10[0], ytop + 0.42), ha="center", fontsize=6.6, color=MUTED)
ax[1].annotate("2014", xy=(t14[0], ytop), xytext=(t14[0], ytop + 0.42), ha="center", fontsize=6.6, color=ORD4[2])
ax[1].set_ylim(-0.6, len(TS) - 0.15)
for a in ax: a.tick_params(labelsize=7)
fig.subplots_adjust(wspace=0.30)
save(fig, "g04_dumbbell")
N["area"] = dict(tt=[round(v, 1) for v in [v10[0], v14[0]]], nt=[round(v, 1) for v in [v10[1], v14[1]]])
N["tier"] = {t: [round(a, 1), round(b, 1), round((b/a - 1)*100)] for t, a, b in zip(TS, t10, t14)}

# =====================================================================  2. CHI TIÊU
# ---- g05: gánh nặng thiết yếu
fig, ax = plt.subplots(1, 2, figsize=(8.16, 1.7), gridspec_kw=dict(width_ratios=[1.15, 1]))
nec_t = {q: [(d[(d.Year == y) & (d.Quart == q)].nec / d[(d.Year == y) & (d.Quart == q)].income).median()*100 for y in Y] for q in QS}
for q, c in zip(QS, ORD4):
    ax[0].plot(Y, nec_t[q], "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[0].text(2014.12, nec_t[q][2], f"Q{q}  {vn(nec_t[q][2],0)}%", color=c if q > 1 else "#6380c8", fontsize=7, va="center")
ax[0].set_xticks(Y); ax[0].set_xlim(2009.6, 2015.2); ax[0].set_ylim(30, 100)
ax[0].set_ylabel("chi thiết yếu / thu nhập (median, %)")
ax[0].yaxis.set_major_formatter(pct_fmt()); ax[0].set_title("a) Line chart · chi thiết yếu / thu nhập", fontsize=7.6)
necs = [(d[(d.Year == 2014) & (d.Quart == q)].nec / d[(d.Year == 2014) & (d.Quart == q)].income).median()*100 for q in QS]
unns = [(d[(d.Year == 2014) & (d.Quart == q)].unn / d[(d.Year == 2014) & (d.Quart == q)].income).median()*100 for q in QS]
xs = np.arange(4)
b1 = ax[1].bar(xs, necs, 0.55, color="#6380c8", edgecolor=SURF, lw=1.2, zorder=3, label="chi thiết yếu")
b2 = ax[1].bar(xs, unns, 0.55, bottom=necs, color="#f0b49a", edgecolor=SURF, lw=1.2, zorder=3, label="chi chưa thiết yếu")
for i in range(4):
    ax[1].text(i, necs[i]/2, vn(necs[i], 0), ha="center", va="center", fontsize=7, color="white")
    ax[1].text(i, necs[i] + unns[i]/2, vn(unns[i], 0), ha="center", va="center", fontsize=7, color=INK2)
    ax[1].text(i, necs[i] + unns[i] + 2.5, vn(necs[i] + unns[i], 0) + "%", ha="center", fontsize=7, color=INK)
ax[1].axhline(100, color=CORAL, lw=1.4, ls=(0, (4, 3)), zorder=4)
ax[1].text(1.5, 101.5, "100% thu nhập", color=CORAL, fontsize=6.8, ha="center")
ax[1].set_xticks(xs); ax[1].set_xticklabels([f"Q{q}" for q in QS]); ax[1].set_ylim(0, 132)
ax[1].set_ylabel("% thu nhập (median, 2014)"); ax[1].yaxis.set_major_formatter(pct_fmt())
ax[1].legend(loc="upper right", ncol=1); ax[1].set_title("b) Stacked bar · cộng cả rổ chi (2014)", fontsize=7.6)
for a in ax: a.tick_params(labelsize=7)
save(fig, "g05_burden")
N["nec"] = {f"Q{q}": [round(v) for v in nec_t[q]] for q in QS}
N["stack14"] = dict(nec=[round(v) for v in necs], unn=[round(v) for v in unns], tot=[round(a + b) for a, b in zip(necs, unns)])

# ---- g06: bao nhiêu hộ chi vượt thu, vượt bao nhiêu
fig, ax = plt.subplots(1, 2, figsize=(8.16, 1.7))
w = 0.26
for i, (y, c) in enumerate(zip(Y, ORD3)):
    v = [d[(d.Year == y) & (d.Quart == q)].ov.mean()*100 for q in QS]
    r = ax[0].bar(np.arange(4) + (i - 1)*w, v, w, color=c, edgecolor=SURF, lw=1.1, zorder=3, label=str(y))
    label_bars(ax[0], r, lambda t: vn(t, 0), dy=1.0, size=6.2)
ax[0].set_xticks(np.arange(4)); ax[0].set_xticklabels([f"Q{q}" for q in QS]); ax[0].set_ylim(0, 78)
ax[0].set_ylabel("% hộ có tổng chi > thu nhập"); ax[0].yaxis.set_major_formatter(pct_fmt())
ax[0].legend(loc="upper right", ncol=3); ax[0].set_title("a) Grouped bar · tỷ lệ hộ vượt thu", fontsize=7.6)
g = d[d.Year == 2014]
over = [-((g[(g.Quart == q) & g.ov].tot - g[(g.Quart == q) & g.ov].income) / g[(g.Quart == q) & g.ov].income).median()*100 for q in QS]
surp = [((g[(g.Quart == q) & ~g.ov].income - g[(g.Quart == q) & ~g.ov].tot) / g[(g.Quart == q) & ~g.ov].income).median()*100 for q in QS]
r1 = ax[1].bar(xs, over, 0.5, color=ROSE, edgecolor=SURF, lw=1.2, zorder=3, label="hộ chi vượt thu: thiếu hụt")
r2 = ax[1].bar(xs, surp, 0.5, color=TEAL, edgecolor=SURF, lw=1.2, zorder=3, label="hộ còn dư: phần dư")
for i in range(4):
    ax[1].text(i, over[i] - 3, vn(-over[i], 0) + "%", ha="center", va="top", fontsize=7, color=ROSE)
    ax[1].text(i, surp[i] + 3, "+" + vn(surp[i], 0) + "%", ha="center", va="bottom", fontsize=7, color=TEAL)
ax[1].axhline(0, color=INK2, lw=1)
ax[1].set_xticks(xs); ax[1].set_xticklabels([f"Q{q}" for q in QS]); ax[1].set_ylim(-62, 62)
ax[1].set_ylabel("chênh lệch thu − chi (median, % thu nhập)")
ax[1].yaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(abs(v), 0) + "%"))
ax[1].legend(loc="lower right", ncol=1, fontsize=6.6)
ax[1].set_title("b) Bar hai chiều · thiếu và dư (2014)", fontsize=7.6)
for a in ax: a.tick_params(labelsize=7)
save(fig, "g06_overspend")
N["ovrate"] = {str(y): [round(d[(d.Year == y) & (d.Quart == q)].ov.mean()*100) for q in QS] for y in Y}
N["over14"] = [round(-v) for v in over]; N["surp14"] = [round(v) for v in surp]

# ---- g07: hộ chi vượt thu nằm ở đâu
fig, ax = plt.subplots(1, 2, figsize=(8.16, 2.46), gridspec_kw=dict(width_ratios=[1, 1.08]))
for i, (y, c) in enumerate(zip(Y, ORD3)):
    v = [d[(d.tier == t) & (d.Year == y) & (d.Quart == 1)].ov.mean()*100 for t in TS]
    r = ax[0].bar(np.arange(4) + (i - 1)*w, v, w, color=c, edgecolor=SURF, lw=1.1, zorder=3, label=str(y))
    label_bars(ax[0], r, lambda t: vn(t, 0), dy=1.0, size=6.2)
ax[0].set_xticks(np.arange(4)); ax[0].set_xticklabels(["T1\nnghèo", "T2", "T3", "T4\ngiàu"])
ax[0].set_ylim(0, 88); ax[0].set_ylabel("% hộ Q1 chi vượt thu"); ax[0].yaxis.set_major_formatter(pct_fmt())
ax[0].legend(loc="upper left", ncol=3); ax[0].set_title("a) Grouped bar · chỉ hộ Q1, theo nhóm tỉnh", fontsize=7.6)
pv = d[d.Quart == 1].groupby("province_name").agg(ov=("ov", "mean"), n=("ov", "size"))
pv = pv[pv.n >= 60].sort_values("ov")
top = pd.concat([pv.tail(6), pv.head(4)])
cols = [CORAL if v >= pv.ov.median() else TEAL for v in top.ov]
r = hbars(ax[1], np.arange(len(top)), top.ov.values*100, "#000", height=0.62)
for rect, c in zip(r, cols): rect.set_color(c)
label_bars(ax[1], r, lambda v: vn(v, 0) + "%", dy=1.0, size=7.2, horizontal=True)
ax[1].set_yticks(np.arange(len(top))); ax[1].set_yticklabels([f"{i}  (n={int(n)})" for i, n in zip(top.index, top.n)], fontsize=6.6)
ax[1].axvline(d[d.Quart == 1].ov.mean()*100, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=4)
ax[1].text(d[d.Quart == 1].ov.mean()*100 + 1, -0.9, f"cả nước {vn(d[d.Quart==1].ov.mean()*100,0)}%", fontsize=6.4, color=MUTED)
ax[1].set_xlim(0, 105); ax[1].grid(False); ax[1].set_xticks([])
ax[1].set_title("b) Hbar · theo tỉnh (gộp 3 năm)", fontsize=7.6)
ax[0].tick_params(labelsize=7.8); ax[1].tick_params(labelsize=7.4)
fig.subplots_adjust(wspace=0.34)
save(fig, "g07_where")
N["ov_tier_q1"] = {t: [round(d[(d.tier == t) & (d.Year == y) & (d.Quart == 1)].ov.mean()*100) for y in Y] for t in TS}
N["ov_prov"] = {i: round(v*100) for i, v in top.ov.items()}
N["ov_area"] = {a: [round(d[(d.area == k) & (d.Year == y)].ov.mean()*100) for y in Y] for a, k in [("tt", 1), ("nt", 2)]}

# ---- g08: hộ chi vượt thu khác hộ khác ở điểm gì (gộp 3 năm, so trong cùng nhóm Q)
fig, ax = plt.subplots(1, 3, figsize=(8.16, 2.46), gridspec_kw=dict(width_ratios=[1, 1, 1.35]))
sz_o = [d[(d.Quart == q) & d.ov]["size"].mean() for q in QS]
sz_n = [d[(d.Quart == q) & ~d.ov]["size"].mean() for q in QS]
r1 = ax[0].bar(xs - 0.18, sz_o, 0.34, color=ROSE, edgecolor=SURF, lw=1.1, zorder=3, label="hộ chi vượt thu")
r2 = ax[0].bar(xs + 0.18, sz_n, 0.34, color=TEAL, edgecolor=SURF, lw=1.1, zorder=3, label="hộ không vượt")
label_bars(ax[0], r1, lambda v: vn(v, 1), dy=0.06, size=6.4); label_bars(ax[0], r2, lambda v: vn(v, 1), dy=0.06, size=6.4)
ax[0].set_xticks(xs); ax[0].set_xticklabels([f"Q{q}" for q in QS]); ax[0].set_ylim(0, 5.9)
ax[0].set_ylabel("số người trong hộ (mean)"); ax[0].legend(loc="upper right", fontsize=6.4)
ax[0].set_title("a) Bar · số người trong hộ", fontsize=7.6)
pc_o = [(d[(d.Quart == q) & d.ov].pc).median()/M for q in QS]
pc_n = [(d[(d.Quart == q) & ~d.ov].pc).median()/M for q in QS]
r1 = ax[1].bar(xs - 0.18, pc_o, 0.34, color=ROSE, edgecolor=SURF, lw=1.1, zorder=3)
r2 = ax[1].bar(xs + 0.18, pc_n, 0.34, color=TEAL, edgecolor=SURF, lw=1.1, zorder=3)
label_bars(ax[1], r1, lambda v: vn(v, 1), dy=0.5, size=6.4); label_bars(ax[1], r2, lambda v: vn(v, 1), dy=0.5, size=6.4)
for i in range(4):
    ax[1].text(i, max(pc_o[i], pc_n[i]) + 5.4, f"×{vn(pc_o[i]/pc_n[i],1)}", ha="center", fontsize=6.4, color=INK2)
ax[1].set_xticks(xs); ax[1].set_xticklabels([f"Q{q}" for q in QS]); ax[1].set_ylim(0, max(pc_o)*1.35)
ax[1].set_ylabel("chi/người/năm (median, triệu)"); ax[1].yaxis.set_major_formatter(num_fmt())
ax[1].set_title("b) Bar · chi/người", fontsize=7.6)
IT = {"med": "Thuốc, viện phí", "fhouse": "Sửa chữa nhà", "aid": "Chi hỗ trợ KCB", "edu": "Giáo dục", "rice": "Gạo",
      "elec": "Điện", "fuel": "Nhiên liệu", "nrice": "Thực phẩm khác", "nfood": "Ngoài ăn uống"}
diff = []
for k, l in IT.items():
    a_ = d[d.ov][k].sum()/d[d.ov].tot.sum()*100; b_ = d[~d.ov][k].sum()/d[~d.ov].tot.sum()*100
    diff.append((l, a_ - b_))
diff.sort(key=lambda t: t[1])
r = hbars(ax[2], np.arange(len(diff)), [v for _, v in diff], "#000", height=0.6)
for rect, (_, v) in zip(r, diff): rect.set_color(ROSE if v > 0 else TEAL)
for i, (l, v) in enumerate(diff):
    ax[2].text(v + (0.15 if v > 0 else -0.15), i, ("+" if v > 0 else "") + vn(v, 1), va="center",
               ha="left" if v > 0 else "right", fontsize=7.0, color=INK2)
ax[2].set_yticks(np.arange(len(diff))); ax[2].set_yticklabels([l for l, _ in diff], fontsize=7.4)
ax[2].axvline(0, color=INK2, lw=1); ax[2].set_xlim(-5.2, 5.2); ax[2].grid(False); ax[2].set_xticks([])
ax[2].set_title("c) Hbar · chênh tỷ trọng chi (điểm %)", fontsize=7.6)
ax[0].tick_params(labelsize=7); ax[1].tick_params(labelsize=7); ax[2].tick_params(labelsize=7.4)
fig.subplots_adjust(wspace=0.42)
save(fig, "g08_behavior")
N["size_ov"] = dict(ov=[round(v, 2) for v in sz_o], no=[round(v, 2) for v in sz_n])
N["pc_ov"] = dict(ov=[round(v, 1) for v in pc_o], no=[round(v, 1) for v in pc_n])
N["diff_share"] = {l: round(v, 1) for l, v in diff}
N["med_inc_ov"] = {f"Q{q}": [round((d[(d.Quart == q) & d.ov].med/d[(d.Quart == q) & d.ov].income).median()*100, 1),
                             round((d[(d.Quart == q) & ~d.ov].med/d[(d.Quart == q) & ~d.ov].income).median()*100, 1)] for q in QS}

# ---- g09: đơn vị nào đúng — đồng hay tỷ trọng?
fig, ax = plt.subplots(1, 3, figsize=(8.16, 1.7))
rice_pc = [d[d.Year == y].rice.sum()/d[d.Year == y]["size"].sum()/M for y in Y]
rice_sh = [d[d.Year == y].rice.sum()/d[d.Year == y].tot.sum()*100 for y in Y]
rice_inc = [d[d.Year == y].rice.sum()/d[d.Year == y].income.sum()*100 for y in Y]
for a, v, ttl, unit, c, fm in [
        (ax[0], rice_pc, "a) Bar · tính bằng ĐỒNG", "triệu đồng/người/năm (bình quân)", "#8dabe4", lambda t: vn(t, 2)),
        (ax[1], rice_sh, "b) Bar · tính bằng TỶ TRỌNG", "% tổng chi tiêu", "#f0b49a", lambda t: vn(t, 1) + "%"),
        (ax[2], rice_inc, "c) Bar · tính bằng % THU NHẬP", "% tổng thu nhập", "#a9d6c6", lambda t: vn(t, 1) + "%")]:
    r = bars(a, np.arange(3), v, c, width=0.5)
    label_bars(a, r, fm, dy=max(v)*0.03, size=7)
    a.set_xticks(np.arange(3)); a.set_xticklabels(Y); a.set_ylim(0, max(v)*1.3)
    a.set_ylabel(unit); a.set_title(ttl, fontsize=7.6); a.tick_params(labelsize=7)
    a.yaxis.set_major_formatter(num_fmt(2) if "đồng" in unit else pct_fmt())
save(fig, "g09_unit")
N["rice_unit"] = dict(pc=[round(v, 2) for v in rice_pc], share=[round(v, 1) for v in rice_sh], inc=[round(v, 1) for v in rice_inc])

# ---- g10: cơ cấu chi Q1 và Q4 (pie) — khung cao, dùng với \sidecards
GROUPS = [("Gạo", ["rice"]), ("Thực phẩm khác", ["nrice"]), ("Ngoài ăn uống", ["nfood"]),
          ("Giáo dục + y tế", ["edu", "med", "hins", "aid"]),
          ("Điện nước, nhiên liệu, nhà, thuốc lá", ["elec", "water", "garb", "fuel", "fhouse", "tobaco"])]
PC = ["#e8b4a0", "#f3d9c4", "#a9c4ea", "#8c6ebd", "#a9d6c6"]
fig = plt.figure(figsize=(5.3, 3.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1], hspace=0.95, wspace=0.02)
pa, pb, pc = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])
g = d[d.Year == 2014]
for a, q in [(pa, 1), (pb, 4)]:
    z = g[g.Quart == q]; vals = [z[cols].sum().sum()/z.tot.sum()*100 for _, cols in GROUPS]
    wedges, _ = a.pie(vals, colors=PC, startangle=90, counterclock=False, radius=0.95,
                      wedgeprops=dict(edgecolor=SURF, linewidth=1.6))
    for i_, (w, v) in enumerate(zip(wedges, vals)):
        th = np.deg2rad((w.theta1 + w.theta2) / 2); rr = 1.14 if i_ % 2 == 0 else 1.54
        x, y = rr*np.cos(th), rr*np.sin(th)
        a.text(x, y, vn(v, 1) + "%", ha="right" if x < -0.05 else ("left" if x > 0.05 else "center"),
               va="center", fontsize=7.4, color=INK2)
    a.set_title(f"{'a' if q == 1 else 'b'}) Pie · rổ chi {'Q1 nghèo' if q == 1 else 'Q4 giàu'} (2014)",
                fontsize=7.6, loc="center", pad=6)
pa.legend([l for l, _ in GROUPS], loc="upper center", bbox_to_anchor=(1.02, -0.02), fontsize=6.8, ncol=2,
          handlelength=0.9, columnspacing=1.2)
shq = {l: [g[g.Quart == q][cols].sum().sum()/g[g.Quart == q].tot.sum()*100 for q in QS] for l, cols in GROUPS}
DY2 = {"Giáo dục + y tế": -1.7, "Điện nước, nhiên liệu, nhà, thuốc lá": 1.7}
for (l, _), c in zip(GROUPS, PC):
    pc.plot(xs, shq[l], "-o", color=c, ms=4.5, mec=SURF, mew=1.2, zorder=3)
    pc.text(3.1, shq[l][3] + DY2.get(l, 0), vn(shq[l][3], 1) + "%", color=INK2, fontsize=7, va="center")
pc.set_xticks(xs); pc.set_xticklabels([f"Q{q}" for q in QS]); pc.set_xlim(-0.25, 4.0)
pc.set_ylabel("% tổng chi tiêu"); pc.yaxis.set_major_formatter(pct_fmt())
pc.set_title("c) Line chart · tỷ trọng đổi dần từ Q1 sang Q4", fontsize=7.6); pc.tick_params(labelsize=7.4)
save(fig, "g10_structure")
N["pie_spend"] = {l: [round(v, 1) for v in shq[l]] for l, _ in GROUPS}

# ---- g11: hàng nào "lên đời" theo thu nhập, hàng nào không
ITEMS = {"rice": "Gạo", "tobaco": "Thuốc lá", "hins": "Bảo hiểm y tế", "med": "Thuốc, viện phí", "aid": "Chi hỗ trợ KCB",
         "fhouse": "Sửa chữa nhà", "garb": "Rác", "edu": "Giáo dục", "water": "Nước", "fuel": "Nhiên liệu",
         "elec": "Điện", "nrice": "Thực phẩm khác", "nfood": "Ngoài ăn uống"}
fig, ax = plt.subplots(1, 2, figsize=(8.16, 2.55), gridspec_kw=dict(width_ratios=[1.1, 1]))
g = d[d.Year == 2014]
rs = []
for k, l in ITEMS.items():
    z = g[g[k] > 0]
    rs.append((l, np.corrcoef(np.log(z[k]/z["size"]), np.log(z.Inc_head))[0, 1], (g[k] > 0).mean()*100))
rs.sort(key=lambda t: t[1])
r = hbars(ax[0], np.arange(len(rs)), [v for _, v, _ in rs], "#000", height=0.62)
for rect, (_, v, _) in zip(r, rs): rect.set_color("#8dabe4" if v >= 0.45 else ("#f0b49a" if v >= 0.25 else "#e0a3b8"))
for i, (l, v, p) in enumerate(rs):
    ax[0].text(v + 0.012, i, vn(v, 2), va="center", fontsize=7.0, color=INK2)
ax[0].set_yticks(np.arange(len(rs))); ax[0].set_yticklabels([l for l, _, _ in rs], fontsize=7.2)
ax[0].set_xlim(0, 0.85); ax[0].grid(False); ax[0].set_xticks([])
ax[0].set_title("a) Hbar · r giữa chi và thu nhập (log)", fontsize=7.4)
SEL = [("rice", "Gạo"), ("tobaco", "Thuốc lá"), ("nfood", "Ngoài ăn uống"), ("edu", "Giáo dục")]
CS = [CORAL, ROSE, BLUE, TEAL]
DY = {"Gạo": 0, "Thuốc lá": 0, "Ngoài ăn uống": 0, "Giáo dục": 1.6}
for (k, l), c in zip(SEL, CS):
    v = [g[g.Quart == q][k].sum()/g[g.Quart == q].tot.sum()*100 for q in QS]
    ax[1].plot(xs, v, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[1].text(3.12, v[3] + DY[l], f"{l}  {vn(v[3],1)}%", color=c, fontsize=6.8, va="center")
ax[1].set_xticks(xs); ax[1].set_xticklabels([f"Q{q}" for q in QS]); ax[1].set_xlim(-0.25, 5.1)
ax[1].set_ylabel("% tổng chi tiêu của nhóm"); ax[1].yaxis.set_major_formatter(pct_fmt())
ax[1].set_title("b) Line chart · tỷ trọng theo nhóm Q", fontsize=7.6)
ax[0].tick_params(labelsize=7.2); ax[1].tick_params(labelsize=7.6)
save(fig, "g11_goods")
N["r_items"] = {l: round(v, 2) for l, v, _ in rs}
N["share_sel"] = {l: [round(g[g.Quart == q][k].sum()/g[g.Quart == q].tot.sum()*100, 1) for q in QS] for k, l in SEL}

# =====================================================================  3. TÀI SẢN
h = df[df.house.notna() & (df.house > 0)].copy()
# ---- g12: giá nhà theo tỉnh
fig, ax = plt.subplots(1, 2, figsize=(8.16, 2.55))
p14 = (h[h.Year == 2014].groupby("province_name").house.median()/M)
n14 = h[h.Year == 2014].groupby("province_name").house.size()
p14 = p14[n14 >= 60]
hi, lo = p14.sort_values(ascending=False).head(10)[::-1], p14.sort_values().head(10)[::-1]
for a, ser, c, ttl in [(ax[0], hi, "#6380c8", "a) Hbar · 10 tỉnh đắt nhất (median, 2014)"),
                       (ax[1], lo, "#e8b4a0", "b) Hbar · 10 tỉnh rẻ nhất (trục nhỏ hơn 10 lần)")]:
    r = hbars(a, np.arange(len(ser)), ser.values, c, height=0.62)
    label_bars(a, r, lambda v: vn(v, 0), dy=max(ser.values)*0.02, size=7.2, horizontal=True)
    a.set_yticks(np.arange(len(ser))); a.set_yticklabels(ser.index, fontsize=7.6)
    a.grid(False); a.set_xticks([]); a.set_xlim(0, max(ser.values)*1.22)
    a.set_title(ttl, fontsize=8.0); a.tick_params(labelsize=7.6)
save(fig, "g12_house_prov")
N["house_hi"] = {i: round(v) for i, v in hi[::-1].items()}; N["house_lo"] = {i: round(v) for i, v in lo[::-1].items()}

# ---- g13: giá nhà tăng và khả năng mua nhà
fig, ax = plt.subplots(1, 3, figsize=(8.16, 1.7), gridspec_kw=dict(width_ratios=[1, 1, 1.1]))
for lab, k, c in [("Thành thị", 1, BLUE), ("Nông thôn", 2, CORAL)]:
    v = [h[(h.Year == y) & (h.area == k)].house.median()/M for y in Y]
    ax[0].plot(Y, v, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[0].text(2014.1, v[2], f"{lab}\n{vn(v[2],0)}", color=c, fontsize=6.8, va="center")
ax[0].set_xticks(Y); ax[0].set_xlim(2009.7, 2015.6); ax[0].set_ylabel("giá trị nhà (median, triệu đồng)")
ax[0].yaxis.set_major_formatter(num_fmt()); ax[0].set_title("a) Line chart · giá trị nhà ở", fontsize=7.6)
yrs = [(h[h.Year == y].house / h[h.Year == y].income).median() for y in Y]
hn = [(h[(h.Year == y) & (h.province_name == "Hà Nội")].house / h[(h.Year == y) & (h.province_name == "Hà Nội")].income).median() for y in Y]
hc = [(h[(h.Year == y) & (h.province_name == "TP.HCM")].house / h[(h.Year == y) & (h.province_name == "TP.HCM")].income).median() for y in Y]
for v, lab, c, dy in [(yrs, "Cả nước", GRAY, 0), (hc, "TP.HCM", TEAL, -0.9), (hn, "Hà Nội", LAVENDER, 0.9)]:
    ax[1].plot(Y, v, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[1].text(2014.12, v[2] + dy, f"{lab} {vn(v[2],1)}", color=c, fontsize=6.8, va="center")
ax[1].set_xticks(Y); ax[1].set_xlim(2009.7, 2015.8); ax[1].set_ylim(0, 17)
ax[1].set_ylabel("giá nhà bằng mấy năm thu nhập cả hộ"); ax[1].set_title("b) Line chart · nhà = mấy năm thu nhập", fontsize=7.4)
gr = ((h[h.Year == 2014].groupby("province_name").house.median() / h[h.Year == 2010].groupby("province_name").house.median()) - 1)*100
gr = gr.dropna().sort_values()
ax[2].hist(gr.values, bins=14, color="#a9c4ea", edgecolor=SURF, linewidth=0.8, zorder=3)
ax[2].axvline(gr.median(), color=CORAL, lw=1.6, zorder=4)
ax[2].text(gr.median() + 5, ax[2].get_ylim()[1]*0.88, f"median {vn(gr.median(),0)}%", color=CORAL, fontsize=6.8)
ax[2].set_xlabel("% tăng giá trị nhà 2010 → 2014 của tỉnh"); ax[2].set_ylabel("số tỉnh")
ax[2].xaxis.set_major_formatter(pct_fmt()); ax[2].set_title("c) Histogram · mức tăng của 63 tỉnh", fontsize=7.6)
for a in ax: a.tick_params(labelsize=7)
fig.subplots_adjust(wspace=0.38)
save(fig, "g13_house_growth")
N["house_area"] = {lab: [round(h[(h.Year == y) & (h.area == k)].house.median()/M) for y in Y] for lab, k in [("tt", 1), ("nt", 2)]}
N["house_years"] = dict(all=[round(v, 1) for v in yrs], hn=[round(v, 1) for v in hn], hcm=[round(v, 1) for v in hc])
N["house_growth"] = dict(median=round(gr.median()), lo=round(gr.min()), hi=round(gr.max()), lo_name=gr.index[0], hi_name=gr.index[-1])

# ---- g14: scatter — nhà với thu nhập, nhà với tiền sửa nhà
fig, ax = plt.subplots(1, 2, figsize=(8.16, 1.7))
z = h[(h.Year == 2014) & h.Inc_head.notna()]
ax[0].scatter(z.Inc_head/M, z.house/M, s=3.5, color=BLUE, alpha=0.16, linewidths=0, zorder=3)
ax[0].set_xscale("log"); ax[0].set_yscale("log")
r0 = np.corrcoef(np.log(z.Inc_head), np.log(z.house))[0, 1]
ax[0].set_xlabel("thu nhập/người/năm (triệu, thang log)"); ax[0].set_ylabel("giá trị nhà (triệu, thang log)")
ax[0].set_title(f"a) Scatterplot — nhà ở và thu nhập: r = {vn(r0,2)}", fontsize=7.6)
for q, c in zip(QS, ORD4):
    zz = z[z.Quart == q]; ax[0].plot([zz.Inc_head.median()/M], [zz.house.median()/M], "o", ms=8, color=c, mec=SURF, mew=1.4, zorder=5)
ax[0].text(0.03, 0.93, "chấm to = median của Q1…Q4", transform=ax[0].transAxes, fontsize=6.4, color=INK2)
f = z[z.fhouse > 0]
ax[1].scatter(f.house/M, f.fhouse/M, s=5, color=LAVENDER, alpha=0.3, linewidths=0, zorder=3)
ax[1].set_xscale("log"); ax[1].set_yscale("log")
r1_ = np.corrcoef(np.log(f.house), np.log(f.fhouse))[0, 1]
ax[1].set_xlabel("giá trị nhà (triệu, thang log)"); ax[1].set_ylabel("chi sửa/xây nhà trong năm (triệu, log)")
ax[1].set_title(f"b) Scatterplot — nhà to có sửa nhiều hơn không? r = {vn(r1_,2)}", fontsize=7.6)
ax[1].text(0.03, 0.06, f"chỉ {vn((z.fhouse>0).mean()*100,0)}% hộ có chi sửa nhà trong năm", transform=ax[1].transAxes, fontsize=6.4, color=INK2)
for a in ax: a.tick_params(labelsize=7); a.grid(True, axis="both", color=GRID, lw=0.6)
save(fig, "g14_scatter")
N["r_house_inc"] = round(r0, 2); N["r_house_fhouse"] = round(r1_, 2); N["fhouse_pct"] = round((z.fhouse > 0).mean()*100, 1)

# ---- g15: tài sản nào phản ánh giàu nghèo rõ nhất
fig, ax = plt.subplots(1, 3, figsize=(8.16, 1.7), gridspec_kw=dict(width_ratios=[1.15, 1, 1])); t = df[df.Year == 2014]
OWN = [("hmachine", "Máy\ngia dụng"), ("tv", "TV"), ("tele", "Điện\nthoại"), ("moto", "Xe\nmáy"), ("emachine", "Máy\ngiải trí"), ("oto", "Ô tô")]
for i, (q, c) in enumerate(zip(QS, ORD4)):
    v = [(t[t.Quart == q][k] > 0).mean()*100 for k, _ in OWN]
    ax[0].bar(np.arange(len(OWN)) + (i - 1.5)*0.2, v, 0.2, color=c, edgecolor=SURF, lw=0.9, zorder=3, label=f"Q{q}")
ax[0].set_xticks(np.arange(len(OWN))); ax[0].set_xticklabels([l for _, l in OWN], fontsize=5.9)
ax[0].set_ylabel("% hộ sở hữu (2014)"); ax[0].yaxis.set_major_formatter(pct_fmt()); ax[0].set_ylim(0, 112)
ax[0].legend(loc="upper right", ncol=4, fontsize=6.4); ax[0].set_title("a) Grouped bar · tỷ lệ hộ sở hữu", fontsize=7.6)
AS = [("house", "Nhà ở"), ("tech", "Đồ công nghệ"), ("furn", "Nội thất"), ("veh", "Phương tiện")]
rv = []
for k, l in AS:
    z2 = t[(t[k] > 0) & t.Inc_head.notna()]
    rv.append((l, np.corrcoef(np.log(z2[k]), np.log(z2.Inc_head))[0, 1]))
rv.sort(key=lambda x: x[1])
r = hbars(ax[1], np.arange(len(rv)), [v for _, v in rv], "#8dabe4", height=0.55)
label_bars(ax[1], r, lambda v: vn(v, 2), dy=0.012, size=7, horizontal=True)
ax[1].set_yticks(np.arange(len(rv))); ax[1].set_yticklabels([l for l, _ in rv], fontsize=7)
ax[1].set_xlim(0, 0.72); ax[1].grid(False); ax[1].set_xticks([])
ax[1].set_title("b) Hbar · r với thu nhập (log)", fontsize=7.6)
tech = {q: [df[(df.Year == y) & (df.Quart == q)].tech.median()/M for y in Y] for q in QS}
for q, c in zip(QS, ORD4):
    ax[2].plot(Y, tech[q], "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[2].text(2014.12, tech[q][2], f"Q{q}  {vn(tech[q][2],1)}", color=c if q > 1 else "#6380c8", fontsize=6.8, va="center")
ax[2].set_xticks(Y); ax[2].set_xlim(2009.7, 2015.5); ax[2].set_ylabel("giá trị đồ công nghệ (median, triệu)")
ax[2].yaxis.set_major_formatter(num_fmt(1)); ax[2].set_title("c) Line chart · giá trị đồ công nghệ", fontsize=7.6)
for a in ax: a.tick_params(labelsize=7)
save(fig, "g15_assets")
N["own"] = {l: [round((t[t.Quart == q][k] > 0).mean()*100) for q in QS] for k, l in OWN}
N["own_area"] = {l: [round((t[t.area == a_][k] > 0).mean()*100) for a_ in (1, 2)] for k, l in OWN}
N["r_assets"] = {l: round(v, 2) for l, v in rv}
N["tech_q"] = {f"Q{q}": [round(v, 1) for v in tech[q]] for q in QS}

json.dump(N, open(f"{ROOT}/presentation/analysis/numbers20.json", "w"), ensure_ascii=False, indent=1)
print("numbers20.json:", len(N), "mục")
