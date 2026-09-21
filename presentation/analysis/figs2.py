# -*- coding: utf-8 -*-
"""Hình cho Bước 4–6 và Mục 5."""
import json, numpy as np, pandas as pd
from matplotlib.patches import Patch
from style import *

df = pd.read_csv(ROOT + "/processed/vhlss_clean.csv")
d = df[df.tot.notna()].copy()
N = {}
SC = {"Toàn quốc": df.area > 0, "Thành thị": df.area == 1, "Nông thôn": df.area == 2,
      "T1": df.tier == "T1", "T2": df.tier == "T2", "T3": df.tier == "T3", "T4": df.tier == "T4"}
SCL = ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"]
def share(g, col): return g[col].sum() / g.tot.sum() * 100
Q = [1, 2, 3, 4]; QL = ["Q1", "Q2", "Q3", "Q4"]; AREAS = ["Thành thị", "Nông thôn"]; TIERS = ["T1", "T2", "T3", "T4"]; YRS = [2010, 2012, 2014]
g14 = df[df.Year == 2014]; a1214 = df[df.Year >= 2012]

# ---------------- D1 nhà
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1.1, 1]})
h = g14[g14.house.notna()]
for i, ar in enumerate(AREAS):
    v = [h[(h.Quart == q) & (h.area_l == ar)].house.median() / 1000 for q in Q]
    r = bars(a, np.arange(4) + (i - 0.5) * 0.36, v, AREA[ar], width=0.34, label=ar)
    label_bars(a, r, lambda z: vn(z), dy=15, size=5.8)
a.set_xticks(np.arange(4), QL); a.set_title("Median giá nhà 2014 (triệu đồng)"); a.yaxis.set_major_formatter(num_fmt()); a.legend(loc="upper left"); a.set_ylim(0, 1350)
names = ["Thành thị", "Nông thôn", "T1", "T2", "T3", "T4"]
data = [h[SC[n].reindex(h.index)].house_to_inc.dropna() for n in names]
bp = b.boxplot(data, widths=0.5, patch_artist=True, showfliers=False, medianprops=dict(color=SURF, lw=1.5), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED))
for p, c in zip(bp["boxes"], [BLUE, ORANGE] + ORD4): p.set_facecolor(c); p.set_edgecolor(c)
b.set_xticks(range(1, 7), ["Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4"]); b.set_title("Nhà / thu nhập năm của hộ (số năm)"); b.yaxis.set_major_formatter(num_fmt())
plt.subplots_adjust(wspace=0.3); save(fig, "f17_D1")
N["D1"] = dict(med={ar: [round(h[(h.Quart == q) & (h.area_l == ar)].house.median()) for q in Q] for ar in AREAS},
               mean_tt=round(h[h.area == 1].house.mean()), med_tt=round(h[h.area == 1].house.median()),
               hi={n: [round(x.quantile(.25), 1), round(x.median(), 1), round(x.quantile(.75), 1)] for n, x in zip(names, data)},
               hi_t4q1=round(h[(h.tier == "T4") & (h.Quart == 1)].house_to_inc.median(), 1))

# ---------------- D2 đồ công nghệ của hộ nghèo
fig, a = plt.subplots(figsize=(3.75, 2.3))
v1 = [g14[SC[n].reindex(g14.index) & (g14.Quart == 1)].tech.median() / 1000 for n in SC]
v4 = [g14[SC[n].reindex(g14.index) & (g14.Quart == 4)].tech.median() / 1000 for n in SC]
r1 = bars(a, np.arange(7) - 0.18, v1, ORD4[0], width=0.34, label="Hộ Q1"); r4 = bars(a, np.arange(7) + 0.18, v4, ORD4[3], width=0.34, label="Hộ Q4")
label_bars(a, r1, lambda z: vn(z, 1), dy=0.08, size=5.6); label_bars(a, r4, lambda z: vn(z, 1), dy=0.08, size=5.6)
a.set_xticks(np.arange(7), SCL, fontsize=6); a.set_title("Median giá trị đồ công nghệ 2014 (triệu đồng)"); a.yaxis.set_major_formatter(num_fmt()); a.legend(loc="upper left", ncols=2); a.set_ylim(0, 7.2)
save(fig, "f18_D2")
N["D2"] = dict(q1={n: round(v, 2) for n, v in zip(SC, v1)}, q4={n: round(v, 2) for n, v in zip(SC, v4)})

# ---------------- D3 công nghệ và thu nhập
t = g14[g14.tech > 0]; lx = np.log(t.Inc_head); ly = np.log(t.tech)
cov = np.cov(lx, ly)[0, 1]; sx, sy = lx.std(), ly.std(); r = cov / (sx * sy)
fig, a = plt.subplots(figsize=(3.75, 2.35))
a.scatter(t.Inc_head / 1000, t.tech / 1000, s=2, color=BLUE, alpha=0.18, lw=0, zorder=3)
a.set_xscale("log"); a.set_yscale("log"); a.grid(True, axis="both")
fmt = FuncFormatter(lambda v, p: vn(v, 0) if v >= 1 else (vn(v, 1) if v >= 0.1 else vn(v, 2)))
a.xaxis.set_major_formatter(fmt); a.yaxis.set_major_formatter(fmt)
a.set_xlabel("Inc_head 2014 (triệu đồng/người/năm, thang log)"); a.set_ylabel("Đồ công nghệ (triệu đồng, log)", fontsize=6.5)
a.text(0.02, 0.97, f"cov(ln x, ln y) = {vn(cov, 3)}\ns(ln x) = {vn(sx, 3)};  s(ln y) = {vn(sy, 3)}\nr = cov / (s·s) = {vn(r, 2)}", transform=a.transAxes, va="top", fontsize=6.5, color=INK2,
       bbox=dict(boxstyle="round,pad=0.35", fc=SURF, ec=GRID))
save(fig, "f19_D3")
scr = {}
for n in SC:
    tt = t[SC[n].reindex(t.index)]; scr[n] = round(np.corrcoef(np.log(tt.Inc_head), np.log(tt.tech))[0, 1], 2)
N["D3"] = dict(cov=round(cov, 3), sx=round(sx, 3), sy=round(sy, 3), r=round(r, 3), r_scope=scr,
               mean_q={q: round(g14[g14.Quart == q].tech.mean()) for q in Q}, med_q={q: round(g14[g14.Quart == q].tech.median()) for q in Q},
               ratio_q={q: round((g14[g14.Quart == q].tech / g14[g14.Quart == q].income).median() * 100, 1) for q in Q},
               own_tele={q: round((a1214[a1214.Quart == q].tele > 0).mean() * 100) for q in Q}, own_tv={q: round((a1214[a1214.Quart == q].tv > 0).mean() * 100) for q in Q})

# ---------------- D4 cơ cấu đồ dùng + bậc thang xe
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.1]})
grp = ["veh", "tech", "hmachine", "furn"]; gl = ["phương tiện", "công nghệ", "gia dụng", "nội thất"]; gc = [BLUE, VIOLET, AQUA, YELLOW]
s = a1214.groupby("Quart")[grp].sum(); s = s.div(s.sum(axis=1), axis=0) * 100
bt = np.zeros(4)
for k, l, c in zip(grp, gl, gc):
    v = s[k].values
    a.bar(np.arange(4), v, bottom=bt, width=0.6, color=c, edgecolor=SURF, linewidth=1.2, zorder=3, label=l)
    for i, (vv, b0) in enumerate(zip(v, bt)):
        if vv >= 7: a.text(i, b0 + vv / 2, vn(vv) + "%", ha="center", va="center", fontsize=6, color=INK)
    bt += v
a.set_xticks(np.arange(4), QL); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 100); a.grid(False)
a.legend(loc="upper center", ncols=4, bbox_to_anchor=(0.5, 1.15), fontsize=6.2, columnspacing=0.8)
own = {k: [(a1214[a1214.Quart == q][k] > 0).mean() * 100 for q in Q] for k in ["moto", "bicycle", "oto"]}
for k, l, c in [("moto", "xe máy", BLUE), ("bicycle", "xe đạp", ORANGE), ("oto", "ô tô", AQUA)]:
    b.plot(np.arange(4), own[k], color=c, marker="o", ms=5, mec=SURF, mew=1.2)
    b.text(3.12, own[k][-1], f"{l} {vn(own[k][-1])}%", va="center", fontsize=6.3, color=INK2)
b.set_xticks(np.arange(4), QL); b.yaxis.set_major_formatter(pct_fmt()); b.set_ylim(0, 100); b.set_xlim(-0.2, 3.9); b.set_title("% hộ có xe (2012–2014)")
plt.subplots_adjust(wspace=0.28); save(fig, "f20_D4")
N["D4"] = dict(comp=s.round(1).to_dict("index"), own={k: [round(x) for x in v] for k, v in own.items()},
               oto_q4_tier={tt: round((a1214[(a1214.Quart == 4) & (a1214.tier == tt)].oto > 0).mean() * 100, 1) for tt in TIERS})

# ---------------- D5 tài sản nào báo hiệu giàu: heatmap tương quan (nhóm công dụng + chi tiết từng món)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("pastelblue", ["#f4f7fd", "#bfd2f3", "#8dabe4", "#6380c8", "#41559e"])
GRP = {"house": ["house"], "veh": ["oto", "moto", "bicycle"], "tech": ["tele", "tv", "emachine"], "hmachine": ["hmachine"], "furn": ["bed", "tab"],
       "durables": ["oto", "moto", "bicycle", "tele", "tv", "emachine", "hmachine", "bed", "tab"]}
for k, cs in GRP.items(): df["g_" + k] = df[cs].sum(axis=1, min_count=1)
g14 = df[df.Year == 2014]
COLS = [("Toàn quốc", g14), ("Thành thị", g14[g14.area == 1]), ("Nông thôn", g14[g14.area == 2])] + \
       [(tt, g14[g14.tier == tt]) for tt in TIERS] + [(str(y), df[df.Year == y]) for y in YRS]
def rcell(g, k):
    z = g[g[k] > 0]
    return np.corrcoef(np.log(z[k]), np.log(z.Inc_head))[0, 1] if len(z) >= 30 else np.nan
def heatmap(rows, name, figsize, gap_before=None):
    """rows: {cột dữ liệu: nhãn}. Hàng sắp theo r toàn quốc; gap_before: nhãn hàng tham chiếu đặt cuối, tách riêng."""
    M = pd.DataFrame({c: {k: rcell(g, k) for k in rows} for c, g in COLS})
    main = [k for k in M.sort_values("Toàn quốc", ascending=False).index if rows[k] != gap_before]
    order = main + [k for k in rows if rows[k] == gap_before]
    own = {k: (g14[k] > 0).mean() * 100 for k in order}
    ys = {k: i + (0.35 if rows[k] == gap_before else 0) for i, k in enumerate(order)}
    fig, a = plt.subplots(figsize=figsize)
    xs = [0, 1.25, 2.25, 3.5, 4.5, 5.5, 6.5, 7.75, 8.75, 9.75]
    for k in order:
        i = ys[k]
        for j, c in enumerate(M.columns):
            v = M.loc[k, c]; na = v != v
            col = LIGHTGRAY if na else cmap(np.clip(v / 0.65, 0, 1))
            a.add_patch(plt.Rectangle((xs[j] - 0.47, i - 0.44), 0.94, 0.88, color=col, lw=0))
            a.text(xs[j], i, "< 30 hộ" if na else vn(v, 2), ha="center", va="center", fontsize=5.4 if na else 6.6, color=MUTED if na else ("white" if v > 0.5 else INK))
        a.text(11.0, i, vn(own[k]) + "%", ha="center", va="center", fontsize=6.4, color=INK2)
    a.set_xlim(-0.6, 11.6); a.set_ylim(max(ys.values()) + 0.5, -2.75)
    a.set_yticks([ys[k] for k in order], [rows[k] for k in order], fontsize=7); a.set_xticks([])
    HEAD = ["Toàn\nquốc", "Thành\nthị", "Nông\nthôn", "T1", "T2", "T3", "T4", "2010", "2012", "2014", "% hộ\ncó"]
    for x, hd in zip(xs + [11.0], HEAD): a.text(x, -0.62, hd, ha="center", va="bottom", fontsize=6.4, color=INK2, linespacing=1.0)
    a.grid(False); [sp.set_visible(False) for sp in a.spines.values()]
    for x0, x1, lab in [(-0.47, 0.47, "2014"), (0.78, 2.72, "2014 · khu vực"), (3.03, 6.97, "2014 · nhóm tỉnh"), (7.28, 10.22, "toàn quốc · theo năm"), (10.55, 11.45, "2014")]:
        a.plot([x0, x1], [-2.05, -2.05], color=BASE, lw=0.8); a.text((x0 + x1) / 2, -2.15, lab, ha="center", va="bottom", fontsize=5.8, color=MUTED)
    save(fig, name)
    return M.loc[order], own
MG, ownG = heatmap({"g_house": "Nhà", "g_veh": "Phương tiện", "g_tech": "Công nghệ", "g_hmachine": "Đồ gia dụng", "g_furn": "Nội thất",
                    "g_durables": "Tổng đồ dùng (không kể nhà)"}, "f21_D5", (5.9, 1.95), gap_before="Tổng đồ dùng (không kể nhà)")
AS = {"house": "nhà", "hmachine": "máy gia dụng", "oto": "ô tô", "tele": "điện thoại", "moto": "xe máy", "tab": "bàn ghế", "tv": "TV", "bed": "giường", "emachine": "máy giải trí", "bicycle": "xe đạp"}
MD, ownD = heatmap(AS, "f21b_D5_detail", (5.9, 2.5))
LG = {"g_house": "Nhà", "g_veh": "Phương tiện", "g_tech": "Công nghệ", "g_hmachine": "Đồ gia dụng", "g_furn": "Nội thất", "g_durables": "Tổng đồ dùng"}
N["D5"] = {LG[k]: round(v, 2) for k, v in MG["Toàn quốc"].items()}
N["D5_heat"] = {LG[k]: {c: (None if MG.loc[k, c] != MG.loc[k, c] else round(MG.loc[k, c], 2)) for c in MG.columns} for k in MG.index}
N["D5_own"] = {LG[k]: round(v, 1) for k, v in ownG.items()}
N["D5_detail"] = {AS[k]: {c: (None if MD.loc[k, c] != MD.loc[k, c] else round(MD.loc[k, c], 2)) for c in MD.columns} for k in MD.index}

# ---------------- E1a: thu nhập theo Q qua năm (chỉ số 2010 = 100) + tỷ trọng thiết yếu (B3)
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.0))
mq = df.groupby(["Quart", "Year"]).Inc_head.median().unstack()
def spread(vals, gap):
    """Giãn vị trí nhãn cuối đường để không chồng nhau (giữ trung bình)."""
    order = np.argsort(vals); pos = np.array(vals, float)[order]
    for k in range(1, len(pos)): pos[k] = max(pos[k], pos[k - 1] + gap)
    pos += np.mean(vals) - pos.mean(); out = np.empty_like(pos); out[order] = pos; return out
ends = [mq.loc[q, 2014] / mq.loc[q, 2010] * 100 for q in Q]; ly = spread(ends, 7)
for qi, q in enumerate(Q):
    idx = mq.loc[q] / mq.loc[q, 2010] * 100
    a.plot(YRS, idx.values, color=ORD4[qi], marker="o", ms=4.5, mec=SURF, mew=1.2)
    a.text(2014.3, ly[qi], f"{QL[qi]} +{vn(idx.values[-1] - 100)}%", va="center", fontsize=6.3, color=INK2)
a.set_ylim(94, 196)
a.set_xticks(YRS, [str(y) for y in YRS]); a.set_xlim(2009.6, 2015.8); a.set_title("Median Inc_head, 2010 = 100"); a.yaxis.set_major_formatter(num_fmt())
for qi, q in enumerate(Q):
    v = [share(d[(d.Quart == q) & (d.Year == y)], "nec") for y in YRS]
    b.plot(YRS, v, color=ORD4[qi], marker="o", ms=4.5, mec=SURF, mew=1.2)
lyb = spread([share(d[(d.Quart == q) & (d.Year == 2014)], "nec") for q in Q], 1.15)
for qi in range(4): b.text(2014.25, lyb[qi], QL[qi], va="center", fontsize=6.3, color=INK2)
b.set_xticks(YRS, [str(y) for y in YRS]); b.set_xlim(2009.6, 2015.0); b.set_title("% chi cho thiết yếu theo năm"); b.yaxis.set_major_formatter(pct_fmt()); b.set_ylim(64, 79)
plt.subplots_adjust(wspace=0.3); save(fig, "f22_E1a")
N["E1"] = dict(growth={q: round((mq.loc[q, 2014] / mq.loc[q, 2010] - 1) * 100, 1) for q in Q},
               nec_year={q: [round(share(d[(d.Quart == q) & (d.Year == y)], "nec"), 1) for y in YRS] for q in Q},
               q1_rice={y: round(share(d[(d.Quart == 1) & (d.Year == y)], "rice"), 1) for y in YRS},
               q1_nfood={y: round(share(d[(d.Quart == 1) & (d.Year == y)], "nfood"), 1) for y in YRS},
               q1_nec_nofuelna=round(share(d[(d.Quart == 1) & (d.Year == 2014) & ~d.fuel_na], "nec"), 1))

# ---------------- E1b: chỉ số hành vi toàn quốc theo năm (small multiples)
IND = [("tỷ trọng gạo", lambda g, dd: share(dd, "rice")), ("% hộ trả phí rác", lambda g, dd: (g.garb > 0).mean() * 100),
       ("% hộ trả tiền nước", lambda g, dd: (g.water > 0).mean() * 100), ("% hộ tự đóng BHYT", lambda g, dd: (g.hins > 0).mean() * 100),
       ("% hộ có điện thoại", lambda g, dd: (g.tele > 0).mean() * 100), ("% hộ có chi thuốc lá", lambda g, dd: (g.tobaco > 0).mean() * 100)]
fig, axs = plt.subplots(1, 6, figsize=(5.9, 1.6))
TW = {"tỷ trọng gạo": "Tỷ trọng\ngạo", "% hộ trả phí rác": "% hộ trả\nphí rác", "% hộ trả tiền nước": "% hộ trả\ntiền nước", "% hộ tự đóng BHYT": "% hộ tự\nđóng BHYT", "% hộ có điện thoại": "% hộ có\nđiện thoại", "% hộ có chi thuốc lá": "% hộ có chi\nthuốc lá"}
e1b = {}
for ax, (lab, f) in zip(axs, IND):
    v = [f(df[df.Year == y], d[d.Year == y]) for y in YRS]; e1b[lab] = [round(x, 1) for x in v]
    ax.plot(YRS, v, color=BLUE, marker="o", ms=4, mec=SURF, mew=1.1)
    ax.set_title(TW[lab], fontsize=6.8, loc="left"); ax.set_xticks(YRS, ["10", "12", "14"]); ax.tick_params(labelsize=6)
    lo, hi = min(v), max(v); pad = (hi - lo) * 0.6 + 1; ax.set_ylim(lo - pad, hi + pad)
    ax.text(2010, v[0] + pad * 0.35, vn(v[0], 1 if v[0] < 10 else 0), ha="center", fontsize=5.8, color=INK2)
    ax.text(2014, v[-1] + pad * 0.35, vn(v[-1], 1 if v[-1] < 10 else 0), ha="center", fontsize=5.8, color=INK2)
    ax.set_yticks([])
plt.subplots_adjust(wspace=0.3); save(fig, "f23_E1b")
N["E1b"] = e1b

# ---------------- E2: thành thị vs nông thôn
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.9))
ma = df.groupby(["area_l", "Year"]).Inc_head.median().unstack()
for ar in AREAS:
    axs[0].plot(YRS, ma.loc[ar] / 1000, color=AREA[ar], marker="o", ms=4.5, mec=SURF, mew=1.2)
    axs[0].text(2014.25, ma.loc[ar, 2014] / 1000, f"{'TT' if ar == 'Thành thị' else 'NT'} +{vn((ma.loc[ar, 2014] / ma.loc[ar, 2010] - 1) * 100)}%", va="center", fontsize=6.2, color=INK2)
axs[0].set_title("Median Inc_head\n(triệu đồng)"); axs[0].set_ylim(0, 40)
for ax, col, ttl in [(axs[1], "garb", "% hộ trả phí rác"), (axs[2], "tele", "% hộ có điện thoại")]:
    for ar in AREAS:
        v = [(df[(df.Year == y) & (df.area_l == ar)][col] > 0).mean() * 100 for y in YRS]
        ax.plot(YRS, v, color=AREA[ar], marker="o", ms=4.5, mec=SURF, mew=1.2, label=ar)
        ax.text(2014.25, v[-1], vn(v[-1]) + "%", va="center", fontsize=6.2, color=INK2)
    ax.set_title(ttl); ax.set_ylim(0, 100); ax.yaxis.set_major_formatter(pct_fmt())
axs[1].legend(loc="center left", fontsize=6)
for ax in axs: ax.set_xticks(YRS, [str(y) for y in YRS]); ax.set_xlim(2009.6, 2015.7)
plt.subplots_adjust(wspace=0.5); save(fig, "f24_E2")
N["E2"] = dict(med={ar: [round(ma.loc[ar, y]) for y in YRS] for ar in AREAS}, ratio=[round(ma.loc["Thành thị", y] / ma.loc["Nông thôn", y], 2) for y in YRS],
               garb={ar: [round((df[(df.Year == y) & (df.area_l == ar)].garb > 0).mean() * 100, 1) for y in YRS] for ar in AREAS},
               water={ar: [round((df[(df.Year == y) & (df.area_l == ar)].water > 0).mean() * 100, 1) for y in YRS] for ar in AREAS},
               tele={ar: [round((df[(df.Year == y) & (df.area_l == ar)].tele > 0).mean() * 100, 1) for y in YRS] for ar in AREAS},
               q4share={ar: [round((df[(df.Year == y) & (df.area_l == ar)].Quart == 4).mean() * 100, 1) for y in YRS] for ar in AREAS})

# ---------------- E3: nhóm tỉnh
fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.9), gridspec_kw={"width_ratios": [1.3, 1, 1]})
mt = df.groupby(["tier", "Year"]).Inc_head.median().unstack()
for ti, tt in enumerate(TIERS):
    axs[0].plot(YRS, mt.loc[tt] / 1000, color=ORD4[ti], marker="o", ms=4.5, mec=SURF, mew=1.2)
    axs[0].text(2014.25, mt.loc[tt, 2014] / 1000, f"{tt} +{vn((mt.loc[tt, 2014] / mt.loc[tt, 2010] - 1) * 100)}%", va="center", fontsize=6.2, color=INK2)
axs[0].set_title("Median Inc_head\n(triệu đồng)"); axs[0].set_xlim(2009.6, 2016.0); axs[0].set_ylim(0, 36)
pm = df.groupby(["Year", "province"]).Inc_head.median().unstack(0)
cvp = pm.std() / pm.mean(); rgp = (pm.max() - pm.min()) / 1000
axs[1].plot(YRS, cvp.values, color=GRAY, marker="o", ms=4.5, mec=SURF, mew=1.2); axs[1].set_title("CV của 63\nmedian tỉnh"); axs[1].set_ylim(0.25, 0.40)
axs[2].plot(YRS, rgp.values, color=GRAY, marker="o", ms=4.5, mec=SURF, mew=1.2); axs[2].set_title("Range của 63 median tỉnh\n(triệu đồng)"); axs[2].set_ylim(0, 40)
for ax, v, dd in [(axs[1], cvp.values, 3), (axs[2], rgp.values, 1)]:
    for x, y in zip(YRS, v): ax.text(x, y + (0.006 if dd == 3 else 1.5), vn(y, dd), ha="center", fontsize=6, color=INK2)
    ax.set_xlim(2009.3, 2014.7)
for ax in axs: ax.set_xticks(YRS, [str(y) for y in YRS])
axs[1].yaxis.set_major_formatter(num_fmt(2))
plt.subplots_adjust(wspace=0.5); save(fig, "f25_E3")
N["E3"] = dict(med={tt: [round(mt.loc[tt, y]) for y in YRS] for tt in TIERS}, growth={tt: round((mt.loc[tt, 2014] / mt.loc[tt, 2010] - 1) * 100, 1) for tt in TIERS},
               t4t1=[round(mt.loc["T4", y] / mt.loc["T1", y], 2) for y in YRS], cv=[round(x, 3) for x in cvp.values], range=[round(x, 1) for x in rgp.values],
               rice={tt: [round(share(d[(d.tier == tt) & (d.Year == y)], "rice"), 1) for y in (2010, 2014)] for tt in TIERS},
               garb={tt: [round((df[(df.tier == tt) & (df.Year == y)].garb > 0).mean() * 100, 1) for y in (2010, 2014)] for tt in TIERS})

# ---------------- E4: từng tỉnh
names = df.groupby("province").province_name.first(); tiers = df.groupby("province").tier.first()
gr = pd.DataFrame({"g": (pm[2014] / pm[2010] - 1) * 100, "g1": (pm[2012] / pm[2010] - 1) * 100, "g2": (pm[2014] / pm[2012] - 1) * 100,
                   "r10": pm[2010].rank(ascending=False), "r14": pm[2014].rank(ascending=False), "name": names, "tier": tiers})
gr["dr"] = gr.r10 - gr.r14
sel = pd.concat([gr.sort_values("g").head(10), gr.sort_values("g").tail(10)])
fig, a = plt.subplots(figsize=(3.6, 2.75))
y = np.arange(len(sel))
rects = hbars(a, y, sel.g.values, [ORD4[TIERS.index(tt)] for tt in sel.tier], height=0.65)
for yy, v in zip(y, sel.g.values): a.text(v + 1.5, yy, vn(v) + "%", va="center", fontsize=6.2, color=INK2)
a.set_yticks(y, sel.name, fontsize=6.4); a.axhline(9.5, color=GRID, lw=0.8); a.set_xlim(0, 140); a.grid(True, axis="x"); a.grid(False, axis="y")
a.set_title("% tăng median Inc_head 2010→2014:\n10 tỉnh cao nhất (trên), thấp nhất (dưới)"); a.xaxis.set_major_formatter(pct_fmt())
a.legend(handles=[Patch(color=c, label=l) for c, l in zip(ORD4, TIERS)], loc="lower right", ncols=2, fontsize=6.2)
save(fig, "f26a_E4")
fig, b = plt.subplots(figsize=(3.6, 2.4))
mv = pd.concat([gr.sort_values("dr").head(5), gr.sort_values("dr").tail(5)])
yy = np.arange(len(mv))
hbars(b, yy, mv.dr.values, [ORANGE if v < 0 else BLUE for v in mv.dr.values], height=0.6)
for y0, v, r10, r14 in zip(yy, mv.dr.values, mv.r10, mv.r14):
    b.text(v + (0.6 if v >= 0 else -0.6), y0, f"{int(r10)} → {int(r14)}", va="center", ha="left" if v >= 0 else "right", fontsize=6.4, color=INK2)
b.set_yticks(yy, mv.name, fontsize=6.6); b.axvline(0, color=BASE, lw=0.8); b.set_xlim(-44, 26); b.grid(True, axis="x"); b.grid(False, axis="y")
b.set_title("Số bậc thay đổi thứ hạng 2010→2014\n(hạng 1 = median cao nhất)")
save(fig, "f26b_E4")
both = gr[(gr.g1 > gr.g1.median()) & (gr.g2 > gr.g2.median())].sort_values("g", ascending=False)
N["E4"] = dict(mean=round(gr.g.mean(), 1), median=round(gr.g.median(), 1), sd=round(gr.g.std(), 1), min=round(gr.g.min(), 1), max=round(gr.g.max(), 1),
               r_periods=round(gr.g1.corr(gr.g2), 2), both=list(both.name), top=list(gr.sort_values("g", ascending=False).head(5).name),
               bottom=list(gr.sort_values("g").head(5).name), up=[(n, int(a_), int(b_)) for n, a_, b_ in zip(mv.tail(5).name, mv.tail(5).r10, mv.tail(5).r14)],
               down=[(n, int(a_), int(b_)) for n, a_, b_ in zip(mv.head(5).name, mv.head(5).r10, mv.head(5).r14)],
               hcm=round(gr.loc[79, "g"], 1), bd=round(gr.loc[74, "g"], 1), top14=list(pm[2014].sort_values(ascending=False).head(5).index.map(names)),
               bot14=list(pm[2014].sort_values().head(5).index.map(names)), max14=round(pm[2014].max()), min14=round(pm[2014].min()))

# ---------------- F1: thu nhập hay nơi ở
e14 = d[d.Year == 2014]
def cell(ar, q): return e14[(e14.area == ar) & (e14.Quart == q)], g14[(g14.area == ar) & (g14.Quart == q)]
IND2 = [("Tỷ trọng thiết yếu", lambda e, g: share(e, "nec")), ("Tỷ trọng thực phẩm", lambda e, g: share(e, "food")), ("Tỷ trọng gạo", lambda e, g: share(e, "rice")),
        ("% hộ tự đóng BHYT", lambda e, g: (g.hins > 0).mean() * 100), ("% hộ trả phí rác", lambda e, g: (g.garb > 0).mean() * 100), ("% hộ trả tiền nước", lambda e, g: (g.water > 0).mean() * 100)]
rows = []
for lab, f in IND2:
    v = {(ar, q): f(*cell(ar, q)) for ar in [1, 2] for q in [1, 4]}
    inc = ((v[(1, 4)] - v[(1, 1)]) + (v[(2, 4)] - v[(2, 1)])) / 2; plc = ((v[(1, 1)] - v[(2, 1)]) + (v[(1, 4)] - v[(2, 4)])) / 2
    rows.append((lab, inc, plc))
fig, a = plt.subplots(figsize=(5.9, 2.3))
y = np.arange(len(rows))[::-1]
ri = hbars(a, y + 0.19, [r_[1] for r_ in rows], BLUE, height=0.36, label="Chênh do thu nhập (Q4 − Q1)")
rp = hbars(a, y - 0.19, [r_[2] for r_ in rows], ORANGE, height=0.36, label="Chênh do nơi ở (thành thị − nông thôn)")
label_bars(a, ri, lambda z: ("+" if z > 0 else "") + vn(z, 1), dy=0.8, size=6, horizontal=True); label_bars(a, rp, lambda z: ("+" if z > 0 else "") + vn(z, 1), dy=0.8, size=6, horizontal=True)
a.set_yticks(y, [r_[0] for r_ in rows]); a.axvline(0, color=BASE, lw=0.8); a.grid(True, axis="x"); a.grid(False, axis="y"); a.set_xlim(-15, 52)
a.set_xlabel("điểm phần trăm (2014)"); a.legend(loc="upper right", fontsize=6.3)
save(fig, "f27_F1")
tech_inc = ((g14[(g14.area == 1) & (g14.Quart == 4)].tech.median() - g14[(g14.area == 1) & (g14.Quart == 1)].tech.median()) + (g14[(g14.area == 2) & (g14.Quart == 4)].tech.median() - g14[(g14.area == 2) & (g14.Quart == 1)].tech.median())) / 2
tech_plc = ((g14[(g14.area == 1) & (g14.Quart == 1)].tech.median() - g14[(g14.area == 2) & (g14.Quart == 1)].tech.median()) + (g14[(g14.area == 1) & (g14.Quart == 4)].tech.median() - g14[(g14.area == 2) & (g14.Quart == 4)].tech.median())) / 2
N["F1"] = dict(rows=[(l, round(i, 1), round(p, 1)) for l, i, p in rows], tech=(round(tech_inc), round(tech_plc)))

# ---------------- I1 + I2: BHYT
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 1.95))
for i, ar in enumerate(AREAS):
    v = [(d[(d.Quart == q) & (d.area_l == ar)].hins > 0).mean() * 100 for q in Q]
    r = bars(a, np.arange(4) + (i - 0.5) * 0.36, v, AREA[ar], width=0.34, label=ar); label_bars(a, r, lambda z: vn(z), dy=1, size=5.8)
a.set_xticks(np.arange(4), QL); a.set_title("% hộ tự đóng BHYT (gộp 3 năm)"); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 92); a.legend(loc="upper left", ncols=2)
mi = d.assign(mi=d.med / d.income * 100)
for i, (lab, m, c) in enumerate([("Có tự đóng BHYT", mi.hins > 0, VIOLET), ("Không tự đóng", mi.hins == 0, GRAY)]):
    v = [mi[m & (mi.Quart == q)].mi.median() for q in Q]
    r = bars(b, np.arange(4) + (i - 0.5) * 0.36, v, c, width=0.34, label=lab); label_bars(b, r, lambda z: vn(z, 1), dy=0.05, size=5.8)
b.set_xticks(np.arange(4), QL); b.set_title("Median chi thuốc, viện phí / thu nhập"); b.yaxis.set_major_formatter(pct_fmt(1)); b.set_ylim(0, 4.6); b.legend(loc="upper right")
plt.subplots_adjust(wspace=0.25); save(fig, "f28_I12")
N["I1"] = dict(p={ar: [round((d[(d.Quart == q) & (d.area_l == ar)].hins > 0).mean() * 100) for q in Q] for ar in AREAS},
               t1q1=round((d[(d.Quart == 1) & (d.tier == "T1")].hins > 0).mean() * 100), nat=[round((df[df.Year == y].hins > 0).mean() * 100, 1) for y in YRS])
cells = {}
for ar in [1, 2]:
    for q in Q:
        g = mi[(mi.area == ar) & (mi.Quart == q)]
        cells[f"{ar}-{q}"] = dict(ins=round(g[g.hins > 0].mi.median(), 2), no=round(g[g.hins == 0].mi.median(), 2), r=round(np.corrcoef(g.hins, g.med)[0, 1], 2), cov=round(np.cov(g.hins, g.med)[0, 1]))
N["I2"] = dict(cells=cells, byQ={q: (round(mi[(mi.hins > 0) & (mi.Quart == q)].mi.median(), 2), round(mi[(mi.hins == 0) & (mi.Quart == q)].mi.median(), 2)) for q in Q})

# ---------------- I3: thuốc lá và y tế
z = g14[(g14.tobaco > 0) & (g14.med > 0)]
fig, a = plt.subplots(figsize=(3.75, 2.3))
a.scatter(z.tobaco / z["size"], z.med / z["size"], s=2, color=BLUE, alpha=0.2, lw=0, zorder=3)
a.set_xscale("log"); a.set_yscale("log"); a.grid(True, axis="both")
a.xaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(v, 0) if v >= 1 else vn(v, 1))); a.yaxis.set_major_formatter(FuncFormatter(lambda v, p: vn(v, 0) if v >= 1 else vn(v, 1)))
a.set_xlabel("Chi thuốc lá / người, 2014 (nghìn đồng, log)"); a.set_ylabel("Chi y tế / người (nghìn, log)", fontsize=6.5)
rq = {}
dz = d[(d.tobaco > 0) & (d.med > 0)]
for q in Q:
    zz = dz[dz.Quart == q]; rq[q] = np.corrcoef(np.log(zz.tobaco / zz["size"]), np.log(zz.med / zz["size"]))[0, 1]
a.text(0.02, 0.97, "r trong từng nhóm Q (gộp 3 năm):\n" + "   ".join(f"Q{q}: {vn(v, 2)}" for q, v in rq.items()), transform=a.transAxes, va="top", fontsize=6.2, color=INK2, bbox=dict(boxstyle="round,pad=0.35", fc=SURF, ec=GRID))
save(fig, "f29_I3")
N["I3"] = {q: round(v, 2) for q, v in rq.items()}

# ---------------- I5 + I6: phí rác theo tỉnh, siêu đô thị
pv = df.groupby("province").agg(urb=("area", lambda s: (s == 1).mean() * 100), garb=("garb", lambda s: (s > 0).mean() * 100), inc=("Inc_head", "median"), name=("province_name", "first"), tier=("tier", "first"))
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.1), gridspec_kw={"width_ratios": [1, 1.25]})
a.scatter(pv.urb, pv.garb, s=14, color=[ORD4[TIERS.index(tt)] for tt in pv.tier], edgecolor=SURF, linewidth=0.8, zorder=3)
for pid in [1, 79]: a.annotate(pv.loc[pid, "name"], (pv.loc[pid, "urb"], pv.loc[pid, "garb"]), xytext=(-6, 4), textcoords="offset points", ha="right", fontsize=6, color=INK2)
a.set_xlabel("% hộ thành thị trong mẫu của tỉnh"); a.set_title("63 tỉnh: % hộ trả phí rác"); a.yaxis.set_major_formatter(pct_fmt()); a.xaxis.set_major_formatter(pct_fmt()); a.grid(True, axis="both")
a.legend(handles=[Patch(color=c, label=l) for c, l in zip(ORD4, TIERS)], loc="lower right", fontsize=5.6, ncols=2)
grp3 = pd.Series(np.where(df.province.isin([1, 79]), "HN + TP.HCM", np.where(df.tier == "T4", "T4 khác", "T1–T3")), index=df.index)
G3 = ["HN + TP.HCM", "T4 khác", "T1–T3"]
m3 = {"Median thu\nnhập (triệu)": [g14[grp3.reindex(g14.index) == k].Inc_head.median() / 1000 for k in G3],
      "% hộ trả\nphí rác": [(df[grp3 == k].garb > 0).mean() * 100 for k in G3],
      "Nhà / thu\nnhập (năm)": [(df[grp3 == k].house_to_inc).median() for k in G3]}
b.axis("off")
inner = b.inset_axes([0, 0, 1, 1]); inner.axis("off")
for j, (lab, vals) in enumerate(m3.items()):
    ax = b.inset_axes([j * 0.35, 0.0, 0.29, 0.82])
    r = bars(ax, np.arange(3), vals, [VIOLET, BLUE, GRAY], width=0.6)
    label_bars(ax, r, lambda z: vn(z, 1 if z < 20 else 0), dy=max(vals) * 0.03, size=5.8)
    ax.set_title(lab, fontsize=6.4, loc="center"); ax.set_xticks(np.arange(3), ["HN+\nHCM", "T4\nkhác", "T1–\nT3"], fontsize=5.8); ax.set_yticks([]); ax.set_ylim(0, max(vals) * 1.22)
save(fig, "f30_I56")
N["I56"] = dict(r_urb=round(pv.urb.corr(pv.garb), 2), r_inc=round(np.log(pv.inc).corr(pv.garb), 2), g3={k: [round(v, 1) for v in vals] for k, vals in m3.items()},
                q4share={k: round((df[grp3 == k].Quart == 4).mean() * 100) for k in G3})

# ---------------- I7 + I8
fig, (a, b) = plt.subplots(1, 2, figsize=(5.9, 2.1), gridspec_kw={"width_ratios": [1, 1.3]})
sz = d["size"].clip(upper=7); pe = (d.edu > 0).groupby(sz).mean() * 100
r = bars(a, np.arange(len(pe)), pe.values, BLUE, width=0.6); label_bars(a, r, lambda z: vn(z), dy=1.5, size=6)
a.set_xticks(np.arange(len(pe)), [str(i) for i in pe.index[:-1]] + ["7+"]); a.set_xlabel("số người trong hộ"); a.set_title("% hộ có chi giáo dục"); a.yaxis.set_major_formatter(pct_fmt()); a.set_ylim(0, 100)
z = df[(df.Year == 2014) & (df.edu > 0)]
pp = z.groupby("province").apply(lambda g: pd.Series({"inc": g.Inc_head.median() / 1000, "edu": (g.edu / g["size"]).median() / 1000, "n": len(g), "tier": g.tier.iloc[0]}), include_groups=False)
b.scatter(pp.inc, pp.edu, s=pp.n.astype(float) * 0.9, color=[ORD4[TIERS.index(tt)] for tt in pp.tier], alpha=0.85, edgecolor=SURF, linewidth=0.8, zorder=3)
b.set_xlabel("Median Inc_head của tỉnh, 2014 (triệu đồng)"); b.set_title("63 tỉnh: chi giáo dục / người (hộ có chi)"); b.grid(True, axis="both"); b.yaxis.set_major_formatter(num_fmt(1))
b.set_ylim(0, 2.75); b.legend(handles=[Patch(color=c, label=l) for c, l in zip(ORD4, TIERS)], loc="upper left", fontsize=5.8, ncols=4)
b.text(0.98, 0.04, "kích thước = số hộ có chi", transform=b.transAxes, ha="right", fontsize=5.8, color=MUTED)
save(fig, "f31_I78")
rr_p, rr_h = {}, {}
for y in YRS:
    zz = df[(df.Year == y) & (df.edu > 0)]
    q_ = zz.groupby("province").apply(lambda g: pd.Series({"inc": g.Inc_head.median(), "edu": (g.edu / g["size"]).median()}), include_groups=False)
    rr_p[y] = round(np.corrcoef(np.log(q_.inc), np.log(q_.edu))[0, 1], 2); rr_h[y] = round(np.corrcoef(np.log(zz.Inc_head), np.log(zz.edu / zz["size"]))[0, 1], 2)
N["I78"] = dict(p_edu={int(k): round(v) for k, v in pe.items()}, size_q=d.groupby("Quart")["size"].mean().round(2).to_dict(), r_prov=rr_p, r_hh=rr_h,
                size_t1q1=round(d[(d.Quart == 1) & (d.tier == "T1")]["size"].mean(), 2))

# ---------------- I9 + I10 + I11
fig, axs = plt.subplots(1, 3, figsize=(5.9, 2.0), gridspec_kw={"width_ratios": [1, 1.05, 0.75]})
for i, ar in enumerate(AREAS):
    v = [d[(d.Quart == q) & (d.area_l == ar)].overspend.mean() * 100 for q in Q]
    r = bars(axs[0], np.arange(4) + (i - 0.5) * 0.36, v, AREA[ar], width=0.34, label=ar)
for qi, q in enumerate(Q):
    top = max(d[(d.Quart == q) & (d.area_l == a_)].overspend.mean() * 100 for a_ in AREAS)
    axs[0].text(qi, top + 2, vn(d[d.Quart == q].overspend.mean() * 100) + "%", ha="center", fontsize=6, color=INK2)
axs[0].set_xticks(np.arange(4), QL); axs[0].set_title("% hộ chi > thu nhập"); axs[0].yaxis.set_major_formatter(pct_fmt()); axs[0].set_ylim(0, 80); axs[0].legend(loc="upper right", fontsize=5.8)
q1 = a1214[a1214.Quart == 1]
ow = pd.Series({l: (q1[k] > 0).mean() * 100 for k, l in [("hmachine", "máy gia dụng"), ("bed", "giường"), ("tv", "TV"), ("tele", "điện thoại"), ("moto", "xe máy"), ("tab", "bàn ghế"), ("bicycle", "xe đạp"), ("emachine", "máy giải trí"), ("oto", "ô tô")]}).sort_values()
cols = [ORANGE if l == "TV" else BLUE for l in ow.index]
r = hbars(axs[1], np.arange(len(ow)), ow.values, cols, height=0.6); label_bars(axs[1], r, lambda z: vn(z) + "%", dy=1.5, size=5.8, horizontal=True)
axs[1].set_yticks(np.arange(len(ow)), ow.index, fontsize=6); axs[1].set_xlim(0, 100); axs[1].grid(True, axis="x"); axs[1].grid(False, axis="y"); axs[1].set_title("Hộ Q1 có từng món"); axs[1].set_xticks([])
v = [(a1214[(a1214.Quart == 4) & (a1214.tier == tt)].oto > 0).mean() * 100 for tt in TIERS]
r = bars(axs[2], np.arange(4), v, ORD4, width=0.55); label_bars(axs[2], r, lambda z: vn(z, 1) + "%", dy=0.15, size=6)
axs[2].set_xticks(np.arange(4), TIERS); axs[2].set_title("Hộ Q4 có ô tô"); axs[2].yaxis.set_major_formatter(pct_fmt()); axs[2].set_ylim(0, 9)
plt.subplots_adjust(wspace=0.75); save(fig, "f32_I9")
N["I9"] = dict(p={ar: [round(d[(d.Quart == q) & (d.area_l == ar)].overspend.mean() * 100) for q in Q] for ar in AREAS}, nat=[round(d[d.Quart == q].overspend.mean() * 100) for q in Q],
               own_q1={k: round(v) for k, v in ow.items()}, oto_q4=[round(x, 1) for x in v],
               inc_share={q: round(g14[g14.Quart == q].income.sum() / g14.income.sum() * 100, 1) for q in Q},
               tot_share={q: round(d[(d.Year == 2014) & (d.Quart == q)].tot.sum() / d[d.Year == 2014].tot.sum() * 100, 1) for q in Q})

json.dump(N, open(ROOT + "/presentation/analysis/numbers2.json", "w"), ensure_ascii=False, indent=1, default=float)
print(json.dumps(N, ensure_ascii=False, default=float)[:9000])
