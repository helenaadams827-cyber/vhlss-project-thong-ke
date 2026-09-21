# -*- coding: utf-8 -*-
import glob
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

ROOT = str(Path(__file__).resolve().parents[2])   # thư mục gốc của project (chứa processed/ và presentation/)

# Be Vietnam Pro: cùng font với slide và trang web
for _f in glob.glob(ROOT + "/presentation/fonts/BeVietnamPro-*.ttf"):
    font_manager.fontManager.addfont(_f)

# Bảng màu pastel (đã chạy validate_palette.py trên nền #F8F9FC: đạt band, chroma, CVD)
SURF = "#fbfbfd"; INK = "#1e2233"; INK2 = "#555b70"; MUTED = "#8a90a3"; GRID = "#e6e8f0"; BASE = "#c9ccd8"
BLUE, CORAL, LAVENDER, TEAL, AMBER, ROSE = "#578ed4", "#ee9370", "#8c6ebd", "#279479", "#d7ac4a", "#d87da2"
SLATE, LIGHTGRAY = "#7a8095", "#dcdee6"
CAT = [BLUE, CORAL, LAVENDER, TEAL, AMBER, ROSE]
# tên cũ trong figs*.py -> màu pastel tương ứng
ORANGE, VIOLET, AQUA, YELLOW, MAGENTA, GREEN, RED = CORAL, LAVENDER, TEAL, AMBER, ROSE, TEAL, SLATE
ORD4 = ["#bfd2f3", "#8dabe4", "#6380c8", "#41559e"]          # Q1..Q4 hoặc T1..T4 (một sắc, nhạt -> đậm)
ORD3 = ["#adc5ef", "#6b8acf", "#41559e"]                      # 2010, 2012, 2014
GRAY = "#b4b8c5"
AREA = {"Thành thị": BLUE, "Nông thôn": CORAL}

plt.rcParams.update({
    "font.family": ["Be Vietnam Pro", "DejaVu Sans"], "font.size": 7.5,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": BASE, "axes.linewidth": 0.8, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 8, "axes.titleweight": "semibold", "axes.titlelocation": "left", "axes.titlepad": 6,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "axes.axisbelow": True,
    "xtick.color": BASE, "ytick.color": BASE, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 4, "ytick.major.pad": 3,
    "legend.frameon": False, "legend.fontsize": 7, "legend.handlelength": 1.0, "legend.handleheight": 0.8,
    "legend.labelcolor": INK2,
    "lines.linewidth": 2, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
    "pdf.fonttype": 42,
})

def vn(x, d=0):
    """Định dạng số kiểu Việt Nam: dấu chấm hàng nghìn, dấu phẩy thập phân."""
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def pct_fmt(d=0): return FuncFormatter(lambda v, p: vn(v, d) + "%")
def num_fmt(d=0): return FuncFormatter(lambda v, p: vn(v, d))

def bars(ax, x, h, color, width=0.6, **kw):
    return ax.bar(x, h, width=width, color=color, edgecolor=SURF, linewidth=1.2, zorder=3, **kw)

def hbars(ax, y, w, color, height=0.6, **kw):
    return ax.barh(y, w, height=height, color=color, edgecolor=SURF, linewidth=1.2, zorder=3, **kw)

def label_bars(ax, rects, fmt, dy=0.0, inside=False, size=6.5, color=INK2, horizontal=False):
    for r in rects:
        if horizontal:
            w = r.get_width(); y = r.get_y() + r.get_height() / 2
            ax.text(w + (dy if w >= 0 else -dy), y, fmt(w), va="center", ha="left" if w >= 0 else "right", fontsize=size, color=color)
        else:
            h = r.get_height(); x = r.get_x() + r.get_width() / 2
            ax.text(x, h + dy, fmt(h), ha="center", va="bottom", fontsize=size, color=color)

def endpoint(ax, x, y, color, text=None, size=6.5, dx=0.08):
    ax.plot([x], [y], "o", ms=5, color=color, mec=SURF, mew=1.5, zorder=5)
    if text is not None:
        ax.text(x + dx, y, text, va="center", ha="left", fontsize=size, color=INK2)

def check_overlaps(fig, name, tol=2.0):
    """Báo các cặp chữ đè nhau (khung bao giao nhau quá tol pixel) — bật bằng CHECK=1."""
    fig.canvas.draw(); r = fig.canvas.get_renderer(); boxes = []
    hidden = set()
    for ax in fig.axes:                                   # nhãn vạch nằm ngoài giới hạn trục không được vẽ
        lo, hi = sorted(ax.get_ylim())
        for tk in ax.yaxis.get_major_ticks():
            if not (lo - 1e-9 <= tk.get_loc() <= hi + 1e-9): hidden.add(id(tk.label1))
        lo, hi = sorted(ax.get_xlim())
        for tk in ax.xaxis.get_major_ticks():
            if not (lo - 1e-9 <= tk.get_loc() <= hi + 1e-9): hidden.add(id(tk.label1))
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip() or id(t) in hidden: continue
        bb = t.get_window_extent(r)
        if bb.width < 1 or bb.height < 1: continue
        boxes.append((bb, t.get_text().replace("\n", " ")[:28]))
    hits = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a_, b_ = boxes[i][0], boxes[j][0]
            w = min(a_.x1, b_.x1) - max(a_.x0, b_.x0); h = min(a_.y1, b_.y1) - max(a_.y0, b_.y0)
            if w > tol and h > tol: hits.append((boxes[i][1], boxes[j][1], round(w), round(h)))
    if hits: print(f"[overlap] {name}: " + " | ".join(f"'{x}' × '{y}' ({w}x{h}px)" for x, y, w, h in hits[:8]))

def save(fig, name):
    import os
    if os.environ.get("CHECK"): check_overlaps(fig, name)
    fig.savefig(f"{ROOT}/presentation/figs/{name}.pdf", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
