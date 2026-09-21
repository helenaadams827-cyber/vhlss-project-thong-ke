# -*- coding: utf-8 -*-
"""Dựng trang web Project Thống Kê: ghép các phần app_*.{html,css,js} và nhúng dữ liệu hộ đã làm sạch.
Chạy:  ../../.venv/bin/python build_web.py   ->  project_thong_ke.html
"""
import json, os, numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))   # thư mục gốc của project
df = pd.read_csv(os.path.join(ROOT, "processed", "vhlss_clean.csv"))

provs = df.groupby("province").agg(name=("province_name", "first"), tier=("tier", "first")).reset_index().sort_values("province")
pidx = {c: i for i, c in enumerate(provs.province)}
MONEY = ["income", "rice", "nrice", "tobaco", "nfood", "edu", "med", "hins", "aid", "water", "elec", "garb", "fuel", "fhouse",
         "house", "oto", "moto", "bicycle", "tele", "tv", "emachine", "hmachine", "bed", "tab"]

def ints(s):
    return [int(v) if v == v else -1 for v in s.round(0)]   # -1 = ô trống

cols = {
    "y": [int(v) for v in df.Year.map({2010: 0, 2012: 1, 2014: 2})],
    "p": [pidx[c] for c in df.province],
    "a": [int(v) for v in df.area],
    "q": [int(v) for v in df.Quart],
    "s": [int(v) for v in df["size"]],
    "f": [int(a) | int(b) << 1 for a, b in zip(df.fuel_na, df.asset_na)],   # bit0 fuel trống, bit1 tài sản trống
}
for c in MONEY: cols[c] = ints(df[c])
data = {"n": len(df), "provinces": [{"code": int(r.province), "name": r["name"], "tier": r.tier} for _, r in provs.iterrows()], "cols": cols}
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
PARTS = ["app_head.html", "app_style.css", "app_body.html", "app_charts.js", "app_engine.js", "app_content.js", "app_main.js"]
def part(n): return open(os.path.join(HERE, n), encoding="utf-8").read()
out = (part("app_head.html") + "<style>\n" + part("app_style.css") + "\n</style>\n" + part("app_body.html")
       + "\n<script>\nconst DATA = " + blob + ";\n</script>\n"
       + "".join("<script>\n" + part(n) + "\n</script>\n" for n in ["app_charts.js", "app_engine.js", "app_content.js", "app_main.js"]))
open(os.path.join(HERE, "project_thong_ke.html"), "w", encoding="utf-8").write(out)
print("rows", len(df), "data MB", round(len(blob.encode()) / 1e6, 2), "page MB", round(len(out.encode()) / 1e6, 2))
