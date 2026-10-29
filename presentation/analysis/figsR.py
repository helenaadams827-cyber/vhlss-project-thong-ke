# -*- coding: utf-8 -*-
"""Hình riêng cho báo cáo chi tiết (report.tex) -> figs/r*.pdf
   Chạy: /home/trang/STATS/.venv/bin/python analysis/figsR.py   (CHECK=1 để dò chữ đè)"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from style import *   # noqa

df = pd.read_csv(f"{ROOT}/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy(); d["ov"] = d.tot > d.income
Y = [2010, 2012, 2014]; QS = [1, 2, 3, 4]; M = 1000.0
g14 = df[df.Year == 2014]

# ---- r01: phân phối thu nhập/người của CẢ 4 NHÓM (2014)
fig, axes = plt.subplots(2, 3, figsize=(7.6, 4.0))
panels = [("Toàn mẫu", g14, "#c9ccd8", 150)] + [(f"Nhóm Q{q}", g14[g14.Quart == q], c, lim)
          for q, c, lim in zip(QS, ORD4, [16, 26, 42, 200])]
for ax, (lab, z, c, lim) in zip(axes.ravel(), panels):
    x = (z.Inc_head/M).clip(upper=lim)
    ax.hist(x, bins=38, color=c, edgecolor=SURF, linewidth=0.4, zorder=3)
    mn, md = z.Inc_head.mean()/M, z.Inc_head.median()/M
    ax.axvline(min(md, lim), color=TEAL, lw=1.4, zorder=4)
    ax.axvline(min(mn, lim), color=CORAL, lw=1.4, zorder=4)
    ax.set_title(f"{lab}  ·  n = {vn(len(z))}", fontsize=8)
    ax.set_xlabel("triệu đồng/người/năm", fontsize=7)
    ax.set_ylabel("số hộ", fontsize=7); ax.yaxis.set_major_formatter(num_fmt())
    ax.tick_params(labelsize=7)
    ax.text(0.97, 0.93, f"median {vn(md,1)}\nmean {vn(mn,1)}\nskew {vn(z.Inc_head.skew(),2)}",
            transform=ax.transAxes, ha="right", va="top", fontsize=6.8, color=INK2)
ax = axes.ravel()[5]
ax.axis("off")
ax.text(0.02, 0.92, "Đọc hình", fontsize=8.5, color=INK, va="top", weight="semibold")
ax.text(0.02, 0.78, "Đường xanh = median, đường cam = mean.\n\n"
        "Q1–Q3: hai đường gần như trùng nhau, phân phối\ncân đối, độ lệch từ −0,21 đến 0,19.\n\n"
        "Q4: mean nằm hẳn bên phải median, đuôi phải kéo\nrất dài (độ lệch 9,8; hộ cao nhất 1.004 triệu).\n\n"
        "Trục hoành mỗi nhóm cắt ở mức khác nhau để\nnhìn được hình dạng; cột cuối gộp các hộ vượt mức.",
        fontsize=7, color=INK2, va="top", linespacing=1.45)
fig.tight_layout(pad=0.6)
save(fig, "r01_dist_q")

# ---- r02: boxplot thu nhập theo Q qua 3 năm
fig, ax = plt.subplots(figsize=(7.4, 2.9))
pos, ticks, labels = [], [], []
for i, q in enumerate(QS):
    for j, (y, c) in enumerate(zip(Y, ORD3)):
        z = (df[(df.Year == y) & (df.Quart == q)].Inc_head/M).values
        bp = ax.boxplot([z], positions=[i*4 + j], widths=0.72, whis=(5, 95), showfliers=False,
                        patch_artist=True, medianprops=dict(color=INK, lw=1.3),
                        whiskerprops=dict(color=BASE, lw=0.9), capprops=dict(color=BASE, lw=0.9),
                        boxprops=dict(edgecolor=SURF, lw=1), zorder=3)
        bp["boxes"][0].set_facecolor(c)
        ax.text(i*4 + j, np.median(z) + 1.5, vn(np.median(z), 1), ha="center", fontsize=6.4, color=INK2)
    ticks.append(i*4 + 1); labels.append(f"Q{q}")
ax.set_xticks(ticks); ax.set_xticklabels(labels); ax.set_xlim(-1, 15)
ax.set_ylabel("thu nhập/người/năm (triệu đồng)"); ax.yaxis.set_major_formatter(num_fmt())
for j, (y, c) in enumerate(zip(Y, ORD3)): ax.bar([0], [0], color=c, label=str(y))
ax.legend(loc="upper left", ncol=3); ax.tick_params(labelsize=7.5)
ax.set_title("Hộp: khoảng tứ phân vị (25–75%), vạch giữa: median, râu: bách phân vị 5 và 95", fontsize=7.6)
save(fig, "r02_box_year")

# ---- r03: thập phân vị
fig, ax = plt.subplots(1, 2, figsize=(7.4, 2.8), gridspec_kw=dict(width_ratios=[1.25, 1]))
w = 0.38
for i, (y, c) in enumerate(zip([2010, 2014], ["#bfd2f3", "#41559e"])):
    z = df[df.Year == y].copy(); z["dec"] = pd.qcut(z.Inc_head.rank(method="first"), 10, labels=False) + 1
    sh = z.groupby("dec").income.sum()/z.income.sum()*100
    r = ax[0].bar(np.arange(10) + (i - 0.5)*w, sh.values, w, color=c, edgecolor=SURF, lw=1, zorder=3, label=str(y))
    if y == 2014: label_bars(ax[0], r, lambda v: vn(v, 1), dy=0.4, size=6.2)
ax[0].set_xticks(np.arange(10)); ax[0].set_xticklabels([f"D{i}" for i in range(1, 11)])
ax[0].set_ylabel("% tổng thu nhập cả nước"); ax[0].yaxis.set_major_formatter(pct_fmt())
ax[0].legend(loc="upper left"); ax[0].tick_params(labelsize=7.5)
ax[0].set_title("a) Mỗi nhóm 10% số hộ giữ bao nhiêu phần thu nhập", fontsize=7.8)
z = df[df.Year == 2014].copy(); z["dec"] = pd.qcut(z.Inc_head.rank(method="first"), 10, labels=False) + 1
sh = z.groupby("dec").income.sum()/z.income.sum()*100
cum = sh.cumsum()
ax[1].plot(np.arange(1, 11)*10, cum.values, "-o", color=BLUE, ms=5, mec=SURF, mew=1.4, zorder=4)
ax[1].plot([0, 100], [0, 100], ls=(0, (4, 3)), color=MUTED, lw=1.2, zorder=3)
ax[1].fill_between(np.arange(1, 11)*10, cum.values, np.arange(1, 11)*10, color="#e6eefa", zorder=2)
ax[1].text(62, 30, "vùng chênh lệch", fontsize=7, color=INK2)
ax[1].text(20, 92, "đường 45°: nếu\nmọi hộ thu nhập\nnhư nhau", fontsize=6.6, color=MUTED, va="top")
ax[1].set_xlabel("% số hộ cộng dồn (từ nghèo nhất)"); ax[1].set_ylabel("% thu nhập cộng dồn")
ax[1].xaxis.set_major_formatter(pct_fmt()); ax[1].yaxis.set_major_formatter(pct_fmt())
ax[1].set_xlim(0, 100); ax[1].set_ylim(0, 100); ax[1].set_xticks([25, 50, 75, 100]); ax[1].set_yticks([25, 50, 75, 100]); ax[1].tick_params(labelsize=7.5)
ax[1].set_title("b) Cộng dồn (2014)", fontsize=7.8)
fig.tight_layout(pad=0.5)
save(fig, "r03_decile")

# ---- r04: độ phân tán trong từng nhóm
fig, ax = plt.subplots(1, 2, figsize=(7.4, 2.7))
DYCV = {1: 0, 2: 2.6, 3: -2.6, 4: 0}
for q, c in zip(QS, ORD4):
    sd = [df[(df.Year == y) & (df.Quart == q)].Inc_head.std(ddof=1)/M for y in Y]
    cv = [df[(df.Year == y) & (df.Quart == q)].Inc_head.std(ddof=1)/df[(df.Year == y) & (df.Quart == q)].Inc_head.mean()*100 for y in Y]
    ax[0].plot(Y, sd, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3, label=f"Q{q}")
    ax[1].plot(Y, cv, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3)
    ax[1].plot([], [], "-o", color=c, ms=5, label=f"Q{q} ({vn(cv[2],0)}%)")
ax[0].set_xticks(Y); ax[0].set_xlim(2009.7, 2014.9); ax[0].set_ylabel("độ lệch chuẩn (triệu đồng)")
ax[0].yaxis.set_major_formatter(num_fmt()); ax[0].legend(loc="upper left", ncol=4); ax[0].set_ylim(0, None)
ax[0].set_title("a) SD trong từng nhóm", fontsize=7.8)
ax[1].set_xticks(Y); ax[1].set_xlim(2009.7, 2014.4); ax[1].set_ylabel("hệ số biến thiên CV")
ax[1].yaxis.set_major_formatter(pct_fmt()); ax[1].legend(loc="center right", fontsize=7, ncol=1)
ax[1].set_title("b) CV = SD / mean, so sánh được giữa các nhóm", fontsize=7.8)
for a in ax: a.tick_params(labelsize=7.5)
fig.tight_layout(pad=0.5)
save(fig, "r04_spread")

# ---- r05: cơ cấu 13 khoản chi theo Q (stacked 100%)
ITEMS = [("rice", "Gạo"), ("nrice", "Thực phẩm khác"), ("nfood", "Ngoài ăn uống"), ("edu", "Giáo dục"),
         ("med", "Thuốc, viện phí"), ("elec", "Điện"), ("fuel", "Nhiên liệu"), ("fhouse", "Sửa nhà"),
         ("tobaco", "Thuốc lá"), ("hins", "BHYT"), ("aid", "Hỗ trợ KCB"), ("water", "Nước"), ("garb", "Rác")]
PAL = ["#e8b4a0", "#f3d9c4", "#a9c4ea", "#8c6ebd", "#d87da2", "#d7ac4a", "#a9d6c6", "#578ed4",
       "#b4b8c5", "#279479", "#ee9370", "#6380c8", "#bfd2f3"]
fig, ax = plt.subplots(figsize=(7.4, 3.1))
g = d[d.Year == 2014]; xs = np.arange(4); bottom = np.zeros(4)
for (k, lab), c in zip(ITEMS, PAL):
    v = np.array([g[g.Quart == q][k].sum()/g[g.Quart == q].tot.sum()*100 for q in QS])
    ax.bar(xs, v, 0.55, bottom=bottom, color=c, edgecolor=SURF, lw=1.1, zorder=3, label=lab)
    for i in range(4):
        if v[i] >= 3.2:
            ax.text(i, bottom[i] + v[i]/2, vn(v[i], 1), ha="center", va="center", fontsize=6.4,
                    color="white" if c in ("#8c6ebd", "#578ed4", "#279479", "#6380c8") else INK2)
    bottom += v
ax.set_xticks(xs); ax.set_xticklabels([f"Q{q}\n(chi/người {vn((g[g.Quart==q].tot/g[g.Quart==q]['size']).median()/M,1)} tr)" for q in QS])
ax.set_ylim(0, 100); ax.set_ylabel("% tổng chi tiêu của nhóm"); ax.yaxis.set_major_formatter(pct_fmt())
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7, handlelength=0.9)
ax.tick_params(labelsize=7.5); ax.grid(False)
ax.set_title("Cơ cấu 13 khoản chi, năm 2014 (số ghi trong cột: % của khoản ≥ 3,2%)", fontsize=7.8)
fig.tight_layout(pad=0.5)
save(fig, "r05_structure13")

# ---- r06: tỷ lệ sở hữu tài sản qua 3 năm, theo khu vực
OWN = [("tele", "Điện thoại"), ("tv", "TV"), ("emachine", "Máy giải trí"), ("hmachine", "Máy gia dụng"),
       ("moto", "Xe máy"), ("oto", "Ô tô")]
fig, ax = plt.subplots(1, 2, figsize=(7.4, 2.8))
for (k, lab), c in zip(OWN, [BLUE, CORAL, LAVENDER, TEAL, AMBER, ROSE]):
    v = [(df[(df.Year == y)][k] > 0).mean()*100 for y in Y]
    ax[0].plot(Y, v, "-o", color=c, ms=5, mec=SURF, mew=1.4, zorder=3, label=f"{lab} ({vn(v[2],0)}%)")
ax[0].legend(loc="center right", fontsize=6.8, ncol=1)
ax[0].set_xticks(Y); ax[0].set_xlim(2009.7, 2014.5); ax[0].set_ylim(0, 112)
ax[0].set_ylabel("% hộ sở hữu"); ax[0].yaxis.set_major_formatter(pct_fmt())
ax[0].set_title("a) Cả nước, 2010 → 2014", fontsize=7.8)
t = df[df.Year == 2014]; w = 0.38
ys = np.arange(len(OWN))[::-1]
for i, (lab, k_) in enumerate([("Thành thị", 1), ("Nông thôn", 2)]):
    v = [(t[t.area == k_][k] > 0).mean()*100 for k, _ in OWN]
    r = ax[1].barh(ys + (0.5 - i)*w, v, w, color=[BLUE, CORAL][i], edgecolor=SURF, lw=1, zorder=3, label=lab)
    label_bars(ax[1], r, lambda x: vn(x, 0), dy=1.2, size=6.2, horizontal=True)
ax[1].set_yticks(ys); ax[1].set_yticklabels([l for _, l in OWN], fontsize=7)
ax[1].set_xlim(0, 118); ax[1].set_xticks([]); ax[1].grid(False)
ax[1].legend(loc="lower right", ncol=1, fontsize=7); ax[1].set_title("b) Thành thị và nông thôn, 2014", fontsize=7.8)
for a in ax: a.tick_params(labelsize=7.5)
fig.tight_layout(pad=0.5)
save(fig, "r06_own_year")
print("xong 6 hình báo cáo")

# =====================================================================  bổ sung: heatmap, boxplot có chấm, Pareto, bubble
from matplotlib.colors import LinearSegmentedColormap
DIV = LinearSegmentedColormap.from_list("div", ["#c96b90", "#e8b4c6", "#f2f3f7", "#a9c4ea", "#41559e"])

# ---- r07: heatmap tương quan (công thức Pearson trên số gốc)
z = d[d.Year == 2014].copy()
VARS = [("Thu nhập/ng", z.Inc_head), ("Tổng chi/ng", z.tot/z["size"]), ("Thực phẩm/ng", z.food/z["size"]),
        ("Ngoài ăn uống", z.nfood/z["size"]), ("Giáo dục/ng", z.edu/z["size"]), ("Y tế/ng", z.health/z["size"]),
        ("Điện nước/ng", z.util/z["size"]), ("Giá trị nhà", z.house), ("Phương tiện", z.veh),
        ("Công nghệ", z.tech), ("Số người/hộ", z["size"])]
M2 = pd.DataFrame({k: v for k, v in VARS}).dropna()
C = M2.corr()
n = len(C)
fig, ax = plt.subplots(figsize=(7.2, 5.4))
mask = np.triu(np.ones_like(C, dtype=bool), k=1)
Cm = np.ma.masked_where(mask, C.values)
im = ax.imshow(Cm, cmap=DIV, vmin=-1, vmax=1)
for i in range(n):
    for j in range(n):
        if j <= i:
            v = C.values[i, j]
            ax.text(j, i, vn(v, 2), ha="center", va="center", fontsize=6.6,
                    color="white" if abs(v) > 0.62 else INK2)
ax.set_xticks(range(n)); ax.set_xticklabels(C.columns, rotation=45, ha="right", fontsize=6.6)
ax.set_yticks(range(n)); ax.set_yticklabels(C.index, fontsize=6.8)
ax.set_xticks(np.arange(-0.5, n, 1), minor=True); ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which="minor", color=SURF, linewidth=1.6); ax.grid(False, which="major")
ax.tick_params(which="both", length=0)
for s_ in ax.spines.values(): s_.set_visible(False)
cb = fig.colorbar(im, ax=ax, shrink=0.55, pad=0.02, ticks=[-1, -0.5, 0, 0.5, 1])
cb.ax.tick_params(labelsize=7, colors=INK2); cb.outline.set_visible(False)
cb.set_label("hệ số tương quan r", fontsize=7, color=INK2)
ax.set_title("Hệ số tương quan Pearson trên số gốc, năm 2014 (n = %s hộ)" % vn(len(M2)), fontsize=8, pad=8)
fig.tight_layout(pad=0.5)
save(fig, "r07_heatmap")

# ---- r08: boxplot + chấm — thu nhập trung vị của 63 tỉnh
pv = df[df.Year == 2014].groupby(["tier", "province_name"]).Inc_head.median()/M
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
rng = np.random.default_rng(3)
for i, t_ in enumerate(["T1", "T2", "T3", "T4"]):
    v = pv.loc[t_].values
    bp = ax[0].boxplot([v], positions=[i], widths=0.52, whis=1.5, showfliers=False, patch_artist=True,
                       medianprops=dict(color=INK, lw=1.3), whiskerprops=dict(color=BASE, lw=0.9),
                       capprops=dict(color=BASE, lw=0.9), boxprops=dict(edgecolor=SURF, lw=1), zorder=2)
    bp["boxes"][0].set_facecolor(ORD4[i]); bp["boxes"][0].set_alpha(0.55)
    ax[0].scatter(i + rng.uniform(-0.16, 0.16, len(v)), v, s=13, color=ORD4[i], edgecolor=SURF,
                  linewidth=0.5, zorder=4)
ax[0].set_xticks(range(4)); ax[0].set_xticklabels(["T1\n(16 tỉnh)", "T2\n(16)", "T3\n(15)", "T4\n(16)"])
ax[0].set_ylabel("median thu nhập/người 2014 (triệu)"); ax[0].yaxis.set_major_formatter(num_fmt())
ax[0].set_title("a) Boxplot + chấm — mỗi chấm là một tỉnh, theo nhóm tỉnh", fontsize=7.8)
allv = pv.droplevel(0)
q1_, q3_ = allv.quantile(0.25), allv.quantile(0.75); iqr = q3_ - q1_
hi_ = q3_ + 1.5*iqr; lo_ = q1_ - 1.5*iqr
bp = ax[1].boxplot([allv.values], positions=[0], widths=0.42, whis=1.5, showfliers=False, patch_artist=True,
                   medianprops=dict(color=INK, lw=1.3), whiskerprops=dict(color=BASE, lw=0.9),
                   capprops=dict(color=BASE, lw=0.9), boxprops=dict(edgecolor=SURF, lw=1), zorder=2)
bp["boxes"][0].set_facecolor("#c9d6ef"); bp["boxes"][0].set_alpha(0.7)
out = allv[(allv > hi_) | (allv < lo_)]
ins = allv[(allv <= hi_) & (allv >= lo_)]
ax[1].scatter(rng.uniform(-0.13, 0.13, len(ins)), ins.values, s=13, color="#6380c8", edgecolor=SURF, linewidth=0.5, zorder=4)
ax[1].scatter(np.zeros(len(out)), out.values, s=34, color=CORAL, edgecolor=SURF, linewidth=0.8, zorder=5)
for nm, v in out.items():
    ax[1].text(0.12, v, f"{nm} {vn(v,1)}", fontsize=6.8, color=CORAL, va="center")
ax[1].axhline(hi_, color=CORAL, lw=1, ls=(0, (4, 3)), zorder=3)
ax[1].text(-0.48, hi_ + 0.8, f"ngưỡng outlier Q3 + 1,5×IQR = {vn(hi_,1)}", fontsize=6.6, color=CORAL)
ax[1].set_xticks([0]); ax[1].set_xticklabels(["Cả 63 tỉnh"]); ax[1].set_xlim(-0.55, 0.95)
ax[1].set_ylabel("median thu nhập/người 2014 (triệu)"); ax[1].yaxis.set_major_formatter(num_fmt())
ax[1].set_title("b) Xét chung: hai tỉnh vượt ngưỡng", fontsize=7.8)
for a in ax: a.tick_params(labelsize=7.2)
fig.tight_layout(pad=0.6)
save(fig, "r08_box_prov")

# ---- r09: boxplot + chấm — giá trị nhà của 63 tỉnh (thay hai biểu đồ cột)
hh = df[(df.Year == 2014) & df.house.notna() & (df.house > 0)]
ph = hh.groupby("province_name").house.median()/M
nprov = hh.groupby("province_name").house.size()
ph = ph[nprov >= 60]
q1_, q3_ = ph.quantile(0.25), ph.quantile(0.75); iqr = q3_ - q1_; hi_ = q3_ + 1.5*iqr
fig, ax = plt.subplots(figsize=(7.4, 2.7))
bp = ax.boxplot([ph.values], positions=[0], widths=0.34, whis=1.5, showfliers=False, patch_artist=True, orientation="horizontal",
                medianprops=dict(color=INK, lw=1.4), whiskerprops=dict(color=BASE, lw=1),
                capprops=dict(color=BASE, lw=1), boxprops=dict(edgecolor=SURF, lw=1), zorder=2)
bp["boxes"][0].set_facecolor("#cfe0d8"); bp["boxes"][0].set_alpha(0.8)
out = ph[ph > hi_]; ins = ph[ph <= hi_]
ax.scatter(ins.values, rng.uniform(-0.12, 0.12, len(ins)), s=15, color=TEAL, edgecolor=SURF, linewidth=0.5, zorder=4)
ax.scatter(out.values, np.zeros(len(out)), s=38, color=CORAL, edgecolor=SURF, linewidth=0.8, zorder=5)
for i_, (nm, v) in enumerate(out.sort_values().items()):
    ax.annotate(f"{nm}\n{vn(v,0)} tr", xy=(v, 0), xytext=(v, 0.22 + 0.13*(i_ % 2)), fontsize=6.8, color=CORAL,
                ha="center", arrowprops=dict(arrowstyle="-", color=CORAL, lw=0.6))
ax.axvline(hi_, color=CORAL, lw=1, ls=(0, (4, 3)), zorder=3)
ax.text(hi_ + 12, -0.42, f"ngưỡng outlier = {vn(hi_,0)} triệu", fontsize=6.8, color=CORAL)
ax.set_yticks([]); ax.set_ylim(-0.55, 0.62); ax.set_xlim(0, 1700)
ax.set_xlabel("median giá trị nhà ở của tỉnh, năm 2014 (triệu đồng) — mỗi chấm là một tỉnh")
ax.xaxis.set_major_formatter(num_fmt()); ax.grid(True, axis="x", color=GRID, lw=0.6); ax.grid(False, axis="y")
ax.set_title("Phân bố giá trị nhà ở giữa các tỉnh: hộp 25–75%, râu 1,5×IQR", fontsize=7.8)
ax.tick_params(labelsize=7.2)
fig.tight_layout(pad=0.5)
save(fig, "r09_box_house")
print("xong heatmap + 2 boxplot")

# ---- r10: Pareto — 13 khoản chi xếp giảm dần + đường tích lũy (cùng một trục %)
ITEMS13 = [("nrice", "Thực phẩm\nkhác"), ("nfood", "Ngoài ăn\nuống"), ("rice", "Gạo"), ("fuel", "Nhiên\nliệu"),
           ("med", "Thuốc,\nviện phí"), ("edu", "Giáo dục"), ("elec", "Điện"), ("fhouse", "Sửa nhà"),
           ("tobaco", "Thuốc lá"), ("aid", "Hỗ trợ\nKCB"), ("hins", "BHYT"), ("water", "Nước"), ("garb", "Rác")]
g = d[d.Year == 2014]
sh = sorted(((g[k].sum()/g.tot.sum()*100, l) for k, l in ITEMS13), reverse=True)
vals = [v for v, _ in sh]; labs = [l for _, l in sh]; cum = np.cumsum(vals)
fig, ax = plt.subplots(figsize=(7.4, 3.0))
r_ = bars(ax, np.arange(13), vals, "#8dabe4", width=0.62)
label_bars(ax, r_, lambda v: vn(v, 1), dy=1.2, size=6.6)
ax.plot(np.arange(13), cum, "-o", color=CORAL, ms=4.5, mec=SURF, mew=1.2, zorder=5)
for i in (3, 5, 12):
    ax.text(i, cum[i] + 3.2, vn(cum[i], 1) + "%", color=CORAL, fontsize=7, ha="center")
ax.axhline(80, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=3)
ax.text(12.4, 82, "mốc 80%", color=MUTED, fontsize=6.8, ha="right")
ax.set_xticks(np.arange(13)); ax.set_xticklabels(labs, fontsize=6.4)
ax.set_ylim(0, 108); ax.set_ylabel("% tổng chi tiêu (cột) và cộng dồn (đường)")
ax.yaxis.set_major_formatter(pct_fmt())
ax.set_title("Biểu đồ Pareto — 4 khoản đầu đã chiếm 81% rổ chi của cả nước (2014)", fontsize=7.8)
ax.tick_params(labelsize=7.2)
fig.tight_layout(pad=0.5)
save(fig, "r10_pareto")

# ---- r11: hộ Q1 vượt thu theo nhóm tỉnh + bubble từng tỉnh
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1, 1.35]))
w = 0.26
for i, (y_, c) in enumerate(zip(Y, ORD3)):
    v = [d[(d.tier == t_) & (d.Year == y_) & (d.Quart == 1)].ov.mean()*100 for t_ in ["T1", "T2", "T3", "T4"]]
    rr = ax[0].bar(np.arange(4) + (i - 1)*w, v, w, color=c, edgecolor=SURF, lw=1.1, zorder=3, label=str(y_))
    label_bars(ax[0], rr, lambda t2: vn(t2, 0), dy=1.0, size=6.2)
ax[0].set_xticks(np.arange(4)); ax[0].set_xticklabels(["T1\nnghèo", "T2", "T3", "T4\ngiàu"])
ax[0].set_ylim(0, 88); ax[0].set_ylabel("% hộ Q1 chi vượt thu"); ax[0].yaxis.set_major_formatter(pct_fmt())
ax[0].legend(loc="upper left", ncol=3, fontsize=6.8)
ax[0].set_title("a) Theo nhóm tỉnh (cỡ mẫu lớn, kết luận vững)", fontsize=7.8)
q1p = d[d.Quart == 1].groupby("province_name").agg(ov=("ov", "mean"), n=("ov", "size"))
inc_p = df[df.Year == 2014].groupby("province_name").Inc_head.median()/M
tier_p = df.groupby("province_name").tier.first()
B = q1p.join(inc_p.rename("inc")).join(tier_p.rename("tier"))
for t_, c in zip(["T1", "T2", "T3", "T4"], ORD4):
    b = B[B.tier == t_]
    ax[1].scatter(b.inc, b.ov*100, s=b.n*0.55, color=c, alpha=0.75, edgecolor=SURF, linewidth=0.8, zorder=3, label=t_)
for nm in ["TP.HCM", "Hà Nội", "Vĩnh Long", "Gia Lai", "Bình Dương"]:
    if nm in B.index:
        b = B.loc[nm]
        ax[1].annotate(nm, xy=(b.inc, b.ov*100), xytext=(b.inc, b.ov*100 + 6), fontsize=6.6, color=INK2, ha="center",
                       arrowprops=dict(arrowstyle="-", color=BASE, lw=0.6))
ax[1].axhline(d[d.Quart == 1].ov.mean()*100, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
ax[1].text(48, d[d.Quart == 1].ov.mean()*100 - 6, "trung bình cả nước", fontsize=6.6, color=MUTED, ha="right")
ax[1].set_xlabel("median thu nhập/người của tỉnh, 2014 (triệu)")
ax[1].set_ylabel("% hộ Q1 chi vượt thu (gộp 3 năm)")
ax[1].yaxis.set_major_formatter(pct_fmt()); ax[1].xaxis.set_major_formatter(num_fmt())
ax[1].set_ylim(10, 100); ax[1].set_xlim(6, 49)
ax[1].legend(loc="lower right", ncol=4, fontsize=6.6, handletextpad=0.1, columnspacing=0.6)
ax[1].set_title("b) Bubble — mỗi chấm một tỉnh, cỡ chấm = số hộ Q1", fontsize=7.8)
for a in ax: a.tick_params(labelsize=7.2)
fig.tight_layout(pad=0.5)
save(fig, "r11_bubble")

# ---- r12: rổ chi của hai loại hộ — mức, chênh lệch theo từng Q, và số tiền
IT12 = [("nrice", "Thực phẩm khác"), ("nfood", "Ngoài ăn uống"), ("rice", "Gạo"), ("fuel", "Nhiên liệu"),
        ("med", "Thuốc, viện phí"), ("edu", "Giáo dục"), ("elec", "Điện"), ("fhouse", "Sửa nhà"),
        ("aid", "Hỗ trợ KCB"), ("tobaco", "Thuốc lá"), ("hins", "BHYT"), ("water", "Nước"), ("garb", "Rác")]
ov, no = d[d.ov], d[~d.ov]
fig, ax = plt.subplots(1, 3, figsize=(7.6, 4.6), gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
ys = np.arange(len(IT12))[::-1]
sa = [ov[k].sum()/ov.tot.sum()*100 for k, _ in IT12]
sb = [no[k].sum()/no.tot.sum()*100 for k, _ in IT12]
ax[0].barh(ys + 0.21, sa, 0.38, color=ROSE, edgecolor=SURF, lw=0.8, zorder=3, label="hộ chi vượt thu")
ax[0].barh(ys - 0.21, sb, 0.38, color=TEAL, edgecolor=SURF, lw=0.8, zorder=3, label="hộ cân đối")
for i, (a_, b_) in enumerate(zip(sa, sb)):
    ax[0].text(a_ + 0.7, ys[i] + 0.21, vn(a_, 1), va="center", fontsize=6.2, color=ROSE)
    ax[0].text(b_ + 0.7, ys[i] - 0.21, vn(b_, 1), va="center", fontsize=6.2, color=TEAL)
ax[0].set_yticks(ys); ax[0].set_yticklabels([l for _, l in IT12], fontsize=6.6)
ax[0].set_xlim(0, 52); ax[0].set_xticks([]); ax[0].grid(False)
ax[0].legend(loc="lower right", fontsize=6.4)
ax[0].set_title("a) Rổ chi của mỗi loại hộ (% tổng chi)", fontsize=7.6)
for i, (k, _) in enumerate(IT12):
    dd = sa[i] - sb[i]
    ax[1].barh(ys[i], dd, 0.52, color=ROSE if dd > 0 else TEAL, edgecolor=SURF, lw=0.8, zorder=3)
    for q in QS:
        za = d[(d.Quart == q) & d.ov]; zb = d[(d.Quart == q) & ~d.ov]
        dq = za[k].sum()/za.tot.sum()*100 - zb[k].sum()/zb.tot.sum()*100
        ax[1].plot([dq], [ys[i]], "o", ms=3.4, color=INK2, alpha=0.75, zorder=5)
ax[1].axvline(0, color=INK2, lw=1)
ax[1].set_yticks(ys); ax[1].set_yticklabels([])
ax[1].set_xlim(-8, 8); ax[1].set_xticks([-6, -3, 0, 3, 6]); ax[1].grid(True, axis="x", color=GRID, lw=0.6)
ax[1].set_xlabel("điểm %", fontsize=6.8)
ax[1].set_title("b) Chênh lệch: cột = gộp,\nchấm = tính riêng trong từng Q", fontsize=7.6)
for i, (k, _) in enumerate(IT12):
    rq = []
    for q in QS:
        za = d[(d.Quart == q) & d.ov]; zb = d[(d.Quart == q) & ~d.ov]
        rq.append((za[k].sum()/za["size"].sum())/(zb[k].sum()/zb["size"].sum()))
    ax[2].plot([min(rq), max(rq)], [ys[i], ys[i]], color=GRID, lw=4, solid_capstyle="round", zorder=2)
    ax[2].plot([rq[0]], [ys[i]], "o", ms=5, color=ORD4[0], mec=SURF, mew=1, zorder=4)
    ax[2].plot([rq[3]], [ys[i]], "o", ms=5, color=ORD4[3], mec=SURF, mew=1, zorder=4)
    ax[2].text(max(rq)*1.12, ys[i], f"{vn(min(rq),1)}–{vn(max(rq),1)}", va="center", fontsize=6, color=INK2)
ax[2].axvline(1, color=CORAL, lw=1, ls=(0, (3, 3)), zorder=3)
ax[2].set_xscale("log"); ax[2].set_xlim(0.8, 30)
ax[2].set_xticks([1, 2, 5, 10]); ax[2].set_xticklabels(["1", "2", "5", "10"])
ax[2].set_yticks(ys); ax[2].set_yticklabels([]); ax[2].grid(True, axis="x", color=GRID, lw=0.6)
ax[2].set_xlabel("số lần (thang log)", fontsize=6.8)
ax[2].plot([], [], "o", ms=5, color=ORD4[0], label="Q1"); ax[2].plot([], [], "o", ms=5, color=ORD4[3], label="Q4")
ax[2].legend(loc="lower right", fontsize=6.4, ncol=2, handletextpad=0.1, columnspacing=0.5)
ax[2].set_title("c) Chi/người bằng tiền:\nhộ vượt thu gấp mấy lần, trong cùng Q", fontsize=7.6)
for a in ax: a.tick_params(labelsize=6.8)
fig.tight_layout(pad=0.5)
save(fig, "r12_basket")
print("xong pareto + bubble + rổ chi")
