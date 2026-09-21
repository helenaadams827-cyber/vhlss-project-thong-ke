/* ============================================================
   Engine — dữ liệu hộ, biểu thức an toàn, truy vấn nhóm
   ============================================================ */
const Eng = (() => {
  const N = DATA.n, C = DATA.cols, PROV = DATA.provinces;
  const YEARS = [2010, 2012, 2014];
  const F = arr => { const a = new Float64Array(N); for (let i = 0; i < N; i++) a[i] = arr[i] < 0 ? NaN : arr[i]; return a; };
  const V = {};                       // biến số (Float64Array) hoặc hàm trả chuỗi
  V.year = Float64Array.from(C.y, v => YEARS[v]);
  V.Q = Float64Array.from(C.q); V.size = Float64Array.from(C.s);
  V.urban = Float64Array.from(C.a, v => v === 1 ? 1 : 0); V.rural = Float64Array.from(C.a, v => v === 2 ? 1 : 0);
  V.tier_no = Float64Array.from(C.p, p => +PROV[p].tier[1]);
  V.fuel_na = Float64Array.from(C.f, v => v & 1); V.asset_na = Float64Array.from(C.f, v => (v >> 1) & 1);
  const MONEY = ["income", "rice", "nrice", "tobaco", "nfood", "edu", "med", "hins", "aid", "water", "elec", "garb", "fuel", "fhouse",
    "house", "oto", "moto", "bicycle", "tele", "tv", "emachine", "hmachine", "bed", "tab"];
  MONEY.forEach(k => V[k] = F(C[k]));
  const add = (ks) => { const a = new Float64Array(N); for (let i = 0; i < N; i++) { let s = 0; for (const k of ks) s += V[k][i]; a[i] = s; } return a; };
  const addz = (ks) => { const a = new Float64Array(N); for (let i = 0; i < N; i++) { let s = 0; for (const k of ks) { const v = V[k][i]; if (v === v) s += v; } a[i] = s; } return a; };
  V.inc_head = Float64Array.from(V.income, (v, i) => v / V.size[i]);
  const FLOWS = ["rice", "nrice", "tobaco", "nfood", "edu", "med", "hins", "aid", "water", "elec", "garb", "fuel", "fhouse"];
  V.tot = add(FLOWS);                                        // NaN khi thiếu nfood
  V.nec = add(["rice", "nrice", "water", "elec", "fuel", "garb", "med", "hins", "aid", "fhouse"]);
  V.unn = add(["nfood", "edu", "tobaco"]);
  V.food = add(["rice", "nrice"]); V.util = add(["elec", "water", "fuel", "garb"]); V.health = add(["med", "hins", "aid"]);
  V.veh = addz(["oto", "moto", "bicycle"]); V.tech = addz(["tele", "tv", "emachine"]); V.furn = addz(["bed", "tab"]);
  V.durables = addz(["oto", "moto", "bicycle", "tele", "tv", "emachine", "hmachine", "bed", "tab"]);
  V.burden = Float64Array.from(V.nec, (v, i) => v / V.income[i]);
  V.overspend = Float64Array.from(V.tot, (v, i) => v === v ? (v > V.income[i] ? 1 : 0) : NaN);
  V.short = Float64Array.from(V.nec, (v, i) => v > V.income[i] ? 1 : 0);
  V.house_to_inc = Float64Array.from(V.house, (v, i) => v / V.income[i]);
  V.save = Float64Array.from(V.tot, (v, i) => (V.income[i] - v) / V.income[i] * 100);
  V.decile = new Float64Array(N);                            // thập phân vị inc_head trong từng năm (1 = 10% thấp nhất)
  YEARS.forEach(y => {
    const ids = []; for (let i = 0; i < N; i++) if (V.year[i] === y) ids.push(i);
    ids.sort((a, b) => V.inc_head[a] - V.inc_head[b] || a - b);
    ids.forEach((i, k) => V.decile[i] = Math.max(1, Math.ceil(k * 10 / (ids.length - 1))));   // giống pd.qcut(rank, 10)
  });
  const S = {                                                // biến chuỗi
    province: i => PROV[C.p[i]].name, tier: i => PROV[C.p[i]].tier,
    area: i => C.a[i] === 1 ? "Thành thị" : "Nông thôn",
  };

  /* ---------- mô tả biến (dùng cho prompt và bảng chọn) */
  const VARS = {
    year: "năm khảo sát (2010, 2012, 2014)", Q: "nhóm thu nhập 1–4 (tứ phân vị Inc_head toàn quốc từng năm; 1 = nghèo nhất)",
    area: "chuỗi 'Thành thị' hoặc 'Nông thôn'", urban: "1 nếu thành thị, 0 nếu nông thôn", rural: "1 nếu nông thôn",
    tier: "nhóm tỉnh, chuỗi 'T1'..'T4' (T1 = nhóm tỉnh nghèo nhất)", tier_no: "nhóm tỉnh dạng số 1–4",
    province: "tên tỉnh (chuỗi, ví dụ 'Hà Nội', 'TP.HCM', 'Đà Nẵng')", size: "số người trong hộ",
    income: "thu nhập cả hộ/năm (nghìn đồng)", inc_head: "thu nhập/người/năm (nghìn đồng) = income/size",
    rice: "chi gạo", nrice: "chi thực phẩm khác gạo", tobaco: "chi thuốc lá", nfood: "chi ngoài ăn uống (quần áo, đi lại, giải trí…)",
    edu: "chi giáo dục", med: "chi thuốc, viện phí", hins: "tiền tự đóng BHYT", aid: "chi hỗ trợ khám chữa bệnh",
    water: "tiền nước", elec: "tiền điện", garb: "phí rác", fuel: "nhiên liệu (ô trống đã điền 0, xem fuel_na)", fhouse: "chi sửa/xây nhà",
    tot: "tổng 13 khoản chi/năm", nec: "chi thiết yếu (Maslow tầng 1–2: rice nrice water elec fuel garb med hins aid fhouse)",
    unn: "chi không thiết yếu (nfood edu tobaco)", food: "rice + nrice", util: "elec + water + fuel + garb", health: "med + hins + aid",
    house: "giá trị nhà đang ở", oto: "giá trị ô tô", moto: "xe máy", bicycle: "xe đạp", tele: "điện thoại", tv: "TV",
    emachine: "máy giải trí", hmachine: "máy gia dụng (tủ lạnh, máy giặt, điều hòa…)", bed: "giường", tab: "bàn ghế",
    veh: "oto+moto+bicycle", tech: "tele+tv+emachine", furn: "bed+tab", durables: "tổng giá trị đồ dùng (không kể nhà)",
    burden: "nec/income (gánh nặng thiết yếu, tỷ số)", overspend: "1 nếu tot > income", short: "1 nếu nec > income (không đủ tiền cho thiết yếu)",
    house_to_inc: "house/income (số năm thu nhập để có căn nhà)", save: "% thu nhập để dành = (income − tot)/income × 100",
    decile: "thập phân vị thu nhập/người trong từng năm, 1–10 (10 = 10% hộ giàu nhất)", fuel_na: "1 nếu ô nhiên liệu bị trống", asset_na: "1 nếu thiếu cả 9 cột tài sản",
  };

  /* ---------- biểu thức: tokenizer + Pratt parser -> closure */
  const FUN = { log: Math.log, ln: Math.log, log10: Math.log10, exp: Math.exp, sqrt: Math.sqrt, abs: Math.abs, min: Math.min, max: Math.max, log1p: Math.log1p };
  function tokenize(src) {
    const t = [], re = /\s*(?:(\d+(?:\.\d+)?)|("[^"]*"|'[^']*')|([A-Za-z_][A-Za-z_0-9]*)|(&&|\|\||==|!=|<=|>=|[-+*/^()<>!,%]))/y;
    let m, pos = 0; src = String(src);
    while (pos < src.length) {
      re.lastIndex = pos; m = re.exec(src);
      if (!m || m[0].length === 0) { if (/^\s*$/.test(src.slice(pos))) break; throw new Error("Không hiểu ký tự ở: " + src.slice(pos, pos + 12)); }
      pos = re.lastIndex;
      if (m[1]) t.push({ k: "num", v: +m[1] }); else if (m[2]) t.push({ k: "str", v: m[2].slice(1, -1) });
      else if (m[3]) { const w = m[3]; t.push(w === "and" ? { k: "op", v: "&&" } : w === "or" ? { k: "op", v: "||" } : w === "not" ? { k: "op", v: "!" } : { k: "id", v: w }); }
      else t.push({ k: "op", v: m[4] });
    }
    return t;
  }
  function compile(src, locals) {
    const tk = tokenize(src); let p = 0;
    const peek = () => tk[p], next = () => tk[p++];
    const BP = { "||": 1, "&&": 2, "==": 3, "!=": 3, "<": 4, "<=": 4, ">": 4, ">=": 4, "+": 5, "-": 5, "*": 6, "/": 6, "%": 6, "^": 7 };
    function nud(t) {
      if (!t) throw new Error("Biểu thức bị thiếu");
      if (t.k === "num") return () => t.v;
      if (t.k === "str") return () => t.v;
      if (t.k === "id") {
        if (peek() && peek().v === "(") {
          next(); const f = FUN[t.v]; if (!f) throw new Error("Không có hàm " + t.v);
          const args = []; if (peek().v !== ")") { do { args.push(expr(0)); } while (peek() && peek().v === "," && next()); }
          if (!peek() || next().v !== ")") throw new Error("Thiếu dấu )");
          return i => f(...args.map(a => a(i)));
        }
        if (locals && locals[t.v]) return locals[t.v];
        if (V[t.v]) { const a = V[t.v]; return i => a[i]; }
        if (S[t.v]) return S[t.v];
        throw new Error("Không có biến " + t.v);
      }
      if (t.v === "(") { const e = expr(0); if (!peek() || next().v !== ")") throw new Error("Thiếu dấu )"); return e; }
      if (t.v === "-") { const e = expr(6.5); return i => -e(i); }
      if (t.v === "!") { const e = expr(6.5); return i => e(i) ? 0 : 1; }
      throw new Error("Không hiểu: " + t.v);
    }
    function expr(rbp) {
      let left = nud(next());
      while (peek() && peek().k === "op" && BP[peek().v] > rbp) {
        const op = next().v, r = expr(op === "^" ? BP[op] - 0.1 : BP[op]), l = left;
        left = {
          "+": i => l(i) + r(i), "-": i => l(i) - r(i), "*": i => l(i) * r(i), "/": i => l(i) / r(i), "%": i => l(i) % r(i), "^": i => Math.pow(l(i), r(i)),
          "<": i => +(l(i) < r(i)), "<=": i => +(l(i) <= r(i)), ">": i => +(l(i) > r(i)), ">=": i => +(l(i) >= r(i)),
          "==": i => +(l(i) == r(i)), "!=": i => +(l(i) != r(i)), "&&": i => +(!!l(i) && !!r(i)), "||": i => +(!!l(i) || !!r(i)),
        }[op];
      }
      return left;
    }
    const f = expr(0); if (p < tk.length) throw new Error("Thừa phần: " + tk.slice(p).map(x => x.v).join(" "));
    return f;
  }

  /* ---------- chiều chia nhóm */
  const SCOPES = ["Toàn quốc", "Thành thị", "Nông thôn", "T1", "T2", "T3", "T4"];
  const DIMS = {
    year: { keys: i => [V.year[i]], order: YEARS, label: v => String(v) },
    Q: { keys: i => [V.Q[i]], order: [1, 2, 3, 4], label: v => "Q" + v },
    area: { keys: i => [S.area(i)], order: ["Thành thị", "Nông thôn"], label: v => v },
    tier: { keys: i => [S.tier(i)], order: ["T1", "T2", "T3", "T4"], label: v => v },
    province: { keys: i => [S.province(i)], order: PROV.map(p => p.name), label: v => v },
    size: { keys: i => [Math.min(7, V.size[i])], order: [1, 2, 3, 4, 5, 6, 7], label: v => v === 7 ? "7+" : String(v) },
    decile: { keys: i => [V.decile[i]], order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label: v => "D" + v },
    scope: { keys: i => ["Toàn quốc", S.area(i), S.tier(i)], order: SCOPES, label: v => v },
    all: { keys: () => ["Toàn quốc"], order: ["Toàn quốc"], label: v => v },
  };
  const DIM_NOTE = "year, Q, area, tier, province, decile (D1–D10), size (7 = 7+ người), scope (mỗi hộ tính vào 'Toàn quốc', khu vực và nhóm tỉnh của nó), all";

  /* ---------- thống kê */
  const sortNum = a => a.sort((x, y) => x - y);
  function quant(sorted, p) { if (!sorted.length) return NaN; const h = (sorted.length - 1) * p, lo = Math.floor(h); return sorted[lo] + (sorted[Math.min(lo + 1, sorted.length - 1)] - sorted[lo]) * (h - lo); }
  function agg(kind, idx, m, fx, fy, fden, fwhere) {
    let rows = idx; if (fwhere) rows = rows.filter(i => fwhere(i));
    if (kind === "count") return { v: rows.length, n: rows.length };
    if (kind === "corr" || kind === "cov") {
      const xs = [], ys = []; for (const i of rows) { const a = fx(i), b = fy(i); if (isFinite(a) && isFinite(b)) { xs.push(a); ys.push(b); } }
      const n = xs.length; if (n < 3) return { v: NaN, n };
      const mx = xs.reduce((s, v) => s + v, 0) / n, my = ys.reduce((s, v) => s + v, 0) / n;
      let sxy = 0, sxx = 0, syy = 0; for (let k = 0; k < n; k++) { const dx = xs[k] - mx, dy = ys[k] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy; }
      return { v: kind === "cov" ? sxy / (n - 1) : sxy / Math.sqrt(sxx * syy), n };
    }
    if (kind === "share" || kind === "ratio") {
      let a = 0, b = 0, n = 0; for (const i of rows) { const x = fx(i), d = fden(i); if (isFinite(x) && isFinite(d)) { a += x; b += d; n++; } }
      return { v: kind === "share" ? a / b * 100 : a / b, n };
    }
    const xs = []; for (const i of rows) { const x = fx(i); if (typeof x === "number" ? isFinite(x) : x != null) xs.push(+x); }
    const n = xs.length; if (!n) return { v: NaN, n: 0 };
    if (kind === "pct") return { v: xs.filter(v => v).length / n * 100, n };
    const sum = xs.reduce((s, v) => s + v, 0), mean = sum / n;
    if (kind === "sum") return { v: sum, n }; if (kind === "mean") return { v: mean, n };
    if (kind === "cv_trim") { const t = sortNum(xs.slice()).slice(0, Math.max(2, Math.floor(n * 0.99))); const mt = t.reduce((a, v) => a + v, 0) / t.length; return { v: Math.sqrt(t.reduce((a, v) => a + (v - mt) ** 2, 0) / (t.length - 1)) / mt, n }; }
    if (kind === "var" || kind === "sd" || kind === "cv") {
      const vr = n > 1 ? xs.reduce((s, v) => s + (v - mean) ** 2, 0) / (n - 1) : NaN;
      return { v: kind === "var" ? vr : kind === "sd" ? Math.sqrt(vr) : Math.sqrt(vr) / mean, n };
    }
    const s = sortNum(xs);
    if (kind === "median") return { v: quant(s, 0.5), n }; if (kind === "min") return { v: s[0], n }; if (kind === "max") return { v: s[n - 1], n };
    if (kind === "range") return { v: s[n - 1] - s[0], n };
    if (kind === "iqr") return { v: quant(s, 0.75) - quant(s, 0.25), n };
    if (kind === "q") return { v: quant(s, m.p != null ? +m.p : 0.5), n };
    if (kind === "skew") { const sd = Math.sqrt(xs.reduce((a, v) => a + (v - mean) ** 2, 0) / (n - 1)); return { v: xs.reduce((a, v) => a + ((v - mean) / sd) ** 3, 0) * n / ((n - 1) * (n - 2)), n }; }
    if (kind === "mode") { const c = new Map(); xs.forEach(v => c.set(v, (c.get(v) || 0) + 1)); let best = NaN, bc = 0; c.forEach((k, v) => { if (k > bc) { bc = k; best = v; } }); return { v: best, n }; }
    throw new Error("Không có phép tính " + kind);
  }
  const AGGS = "count, mean, median, sum, min, max, range, sd, var, cv, cv_trim (CV sau khi bỏ 1% giá trị cao nhất), iqr, q (kèm p, ví dụ 0.9), skew, mode, pct (% hộ có expr khác 0), share (sum(expr)/sum(den)*100), ratio (sum(expr)/sum(den)), sumshare (% của sum(expr) trong nhóm so với tổng mọi nhóm; nếu có where thì % của phần thỏa where trong nhóm), corr / cov (expr với expr2)";

  /* ---------- chạy truy vấn */
  function rowsOf(filter) {
    const f = filter ? compile(filter) : null, out = [];
    for (let i = 0; i < N; i++) if (!f || f(i)) out.push(i);
    return out;
  }
  function run(q) {
    const idx = rowsOf(q.filter);
    const mode = q.mode || "group";
    if (mode === "points") {
      const fx = compile(q.x), fy = compile(q.y), step = Math.max(1, Math.floor(idx.length / (q.sample || 3000)));
      const col = q.color && DIMS[q.color] ? DIMS[q.color] : null, pts = [];
      for (let k = 0; k < idx.length; k += step) { const i = idx[k]; pts.push({ x: fx(i), y: fy(i), g: col ? col.label(col.keys(i)[0]) : null }); }
      return { mode, points: pts, n: idx.length };
    }
    if (mode === "hist") {
      const fx = compile(q.expr); let xs = idx.map(fx).filter(isFinite); if (q.log) xs = xs.filter(v => v > 0).map(Math.log10);
      const s = sortNum(xs.slice()); const lo = q.min != null ? q.min : quant(s, 0.005), hi = q.max != null ? q.max : quant(s, 0.995), nb = q.bins || 30, w = (hi - lo) / nb;
      const bins = Array.from({ length: nb }, (_, k) => ({ x0: lo + k * w, x1: lo + (k + 1) * w, n: 0 }));
      xs.forEach(v => { if (v >= lo && v <= hi) bins[Math.min(nb - 1, Math.floor((v - lo) / w))].n++; });
      return { mode, bins, n: xs.length, log: !!q.log, mean: xs.reduce((a, b) => a + b, 0) / xs.length, median: quant(s, 0.5) };
    }
    const dims = (q.groupBy || []).filter(d => DIMS[d]).slice(0, 2);
    const groups = new Map();
    for (const i of idx) {
      const k1 = dims[0] ? DIMS[dims[0]].keys(i) : ["Toàn quốc"], k2 = dims[1] ? DIMS[dims[1]].keys(i) : [null];
      for (const a of k1) for (const b of k2) { const key = a + "|" + b; let g = groups.get(key); if (!g) groups.set(key, g = { k: [a, b], rows: [] }); g.rows.push(i); }
    }
    if (mode === "box") {
      const fx = compile(q.expr), out = [];
      for (const g of groups.values()) {
        const s = sortNum(g.rows.map(fx).filter(isFinite).filter(v => !q.log || v > 0));
        out.push({ k: g.k, n: s.length, lo: quant(s, 0.1), q1: quant(s, 0.25), med: quant(s, 0.5), q3: quant(s, 0.75), hi: quant(s, 0.9), mean: s.reduce((a, b) => a + b, 0) / s.length });
      }
      sortGroups(out, dims); return { mode, dims, boxes: out };
    }
    let cur = [];
    const loc = {}; (q.measures || []).forEach((_, k) => loc["m" + k] = () => cur[k]);
    const ms = (q.measures || []).map(m => ({ ...m, fx: m.expr ? compile(m.expr) : null, fy: m.expr2 ? compile(m.expr2) : null, fden: m.den ? compile(m.den) : null, fw: m.where ? compile(m.where) : null, fc: m.calc ? compile(m.calc, loc) : null }));
    const out = [];
    const grand = ms.map(m => { if (m.agg !== "sumshare" || m.where) return NaN; let t = 0; for (const i of idx) { const v = m.fx(i); if (isFinite(v)) t += v; } return t; });
    for (const g of groups.values()) {
      const vals = [], ns = []; cur = vals;
      ms.forEach((m, j) => {
        if (m.fc) { vals.push(m.fc(0)); ns.push(g.rows.length); return; }
        if (m.agg === "sumshare") {
          let a = 0, b = 0; for (const i of g.rows) { const v = m.fx(i); if (!isFinite(v)) continue; b += v; if (!m.fw || m.fw(i)) a += v; }
          vals.push(a / (m.fw ? b : grand[j]) * 100); ns.push(g.rows.length); return;
        }
        const r = agg(m.agg || "mean", g.rows, m, m.fx, m.fy, m.fden, m.fw); vals.push(r.v * (m.scale || 1)); ns.push(r.n);
      });
      out.push({ k: g.k, n: g.rows.length, vals, ns });
    }
    sortGroups(out, dims);
    let res = out;
    if (q.sort) { const j = q.sort.by || 0; res = out.slice().sort((a, b) => (q.sort.desc ? -1 : 1) * ((a.vals[j] ?? -Infinity) - (b.vals[j] ?? -Infinity))); }
    const minN = q.minN == null ? 30 : q.minN;
    const nOf = g => q.minNOn != null ? g.ns[q.minNOn] : g.n;
    const small = res.filter(g => nOf(g) < minN).map(g => label(g, dims) + " (" + nOf(g) + " hộ)");
    if (q.dropSmall !== false && dims.includes("province")) res = res.filter(g => nOf(g) >= minN);
    if (q.limit) res = q.limitBoth ? res.slice(0, q.limit).concat(res.slice(-q.limit)) : res.slice(0, q.limit);
    return { mode: "group", dims, measures: ms.map(m => ({ name: m.name || m.agg, agg: m.agg, hide: m.hide, fmt: m.fmt })), groups: res, small, minN, n: idx.length };
  }
  function sortGroups(arr, dims) {
    const ord = d => d ? DIMS[d].order : [null];
    const pos = (d, v) => { const o = ord(d).indexOf(v); return o < 0 ? 1e9 : o; };
    arr.sort((a, b) => pos(dims[0], a.k[0]) - pos(dims[0], b.k[0]) || pos(dims[1], a.k[1]) - pos(dims[1], b.k[1]));
  }
  function label(g, dims) { return dims.map((d, j) => DIMS[d].label(g.k[j])).join(" · ") || "Toàn quốc"; }
  const DIM_LABEL = { decile: "Thập phân vị", year: "Năm", Q: "Nhóm Q", area: "Khu vực", tier: "Nhóm tỉnh", province: "Tỉnh", size: "Số người/hộ", scope: "Phạm vi", all: "Nhóm" };

  /* ---------- màu theo chiều */
  function colorsFor(dim, keys) {
    if (dim === "Q" || dim === "tier") return keys.map(k => ORD[(dim === "Q" ? k : +String(k)[1]) - 1]);
    if (dim === "year") return keys.map(k => ["var(--o1)", "var(--o3)", "var(--o4)"][YEARS.indexOf(k)]);
    if (dim === "area") return keys.map(k => k === "Thành thị" ? "var(--c1)" : "var(--c2)");
    if (dim === "scope") return keys.map(k => SCOPES.indexOf(k) < 3 ? "var(--cgray)" : ORD[+String(k)[1] - 1]);
    if (dim === "province") return keys.map(k => { const p = PROV.find(x => x.name === k); return p ? ORD[+p.tier[1] - 1] : "var(--c1)"; });
    if (dim === "size") return keys.map(() => "var(--c1)");
    if (dim === "decile") return keys.map(k => k >= 10 ? "var(--o4)" : k <= 4 ? "var(--o1)" : "var(--cgray)");
    return keys.map((_, i) => CAT[i % CAT.length]);
  }

  /* ---------- kết quả -> biểu đồ */
  function toChart(r, c = {}) {
    if (r.mode === "points") {
      const groups = [...new Set(r.points.map(p => p.g))].filter(g => g != null);
      const dim = c.colorDim, cols = groups.length ? colorsFor(dim, groups) : [];
      return { type: "scatter", points: r.points.map(p => ({ x: p.x, y: p.y, color: p.g != null ? cols[groups.indexOf(p.g)] : "var(--c1)" })), logx: c.logx, logy: c.logy, xLabel: c.xLabel, yLabel: c.yLabel, fmtx: c.fmtx, fmty: c.fmty, legend: groups.length ? groups.map((g, i) => ({ name: String(g), color: cols[i] })) : null, note: c.note };
    }
    if (r.mode === "hist") {
      const tl = r.log ? (t => fmtNum(Math.pow(10, t), Math.pow(10, t) < 10 ? 1 : 0)) : (t => fmtNum(t / (c.div || 1), 0));
      return { type: "hist", bins: r.bins, xLabel: c.xLabel, tickLabel: tl, binLabel: b => r.log ? fmtNum(Math.pow(10, b.x0) / (c.div || 1), 1) + "–" + fmtNum(Math.pow(10, b.x1) / (c.div || 1), 1) : fmtNum(b.x0 / (c.div || 1), 1) + "–" + fmtNum(b.x1 / (c.div || 1), 1), color: c.color };
    }
    if (r.mode === "box") {
      const d = r.dims[0], keys = r.boxes.map(b => b.k[0]), cols = colorsFor(d, keys);
      return { type: "box", log: c.log, fmt: c.fmt, boxes: r.boxes.map((b, i) => ({ cat: DIMS[d] ? DIMS[d].label(b.k[0]) : "Toàn quốc", ...b, color: cols[i] })) };
    }
    const dims = r.dims, ms = r.measures.map((m, j) => ({ ...m, j })).filter(m => !m.hide), G = r.groups;
    let type = c.type || (dims[0] === "year" ? "line" : dims[0] === "province" ? "hbar" : "bar");
    const fmt = c.fmt || ms[0]?.fmt || (["pct", "share", "sumshare"].includes(ms[0]?.agg) ? "pct" : ["corr"].includes(ms[0]?.agg) ? "r" : null);
    if (type === "scatter") {
      const pts = G.map(g => ({ x: g.vals[ms[0].j], y: g.vals[ms[1].j], r: c.bubble ? Math.max(3, Math.sqrt(g.n) * (c.bubble || 0.45)) : 5, color: colorsFor(dims[0], [g.k[0]])[0], label: (c.labels || []).includes(g.k[0]) ? g.k[0] : null, tip: `<b>${esc(label(g, dims))}</b><br>${esc(ms[0].name)}: ${fmtNum(g.vals[ms[0].j], 1)}<br>${esc(ms[1].name)}: ${fmtNum(g.vals[ms[1].j], 1)}<br>n = ${fmtNum(g.n)}` }));
      return { type: "scatter", points: pts, xLabel: c.xLabel || ms[0].name, yLabel: c.yLabel || ms[1].name, fmtx: c.fmtx, fmty: c.fmty, logx: c.logx, legend: dims[0] === "province" ? ["T1", "T2", "T3", "T4"].map((t, i) => ({ name: t, color: ORD[i] })) : null, note: c.note };
    }
    if (type === "heat") {
      if (dims.length === 2) {
        const rows = [...new Set(G.map(g => g.k[0]))], cols = [...new Set(G.map(g => g.k[1]))];
        const vals = rows.map(a => cols.map(b => { const g = G.find(x => x.k[0] === a && x.k[1] === b); return g && g.n >= r.minN ? g.vals[ms[0].j] : null; }));
        return { type: "heat", rows: rows.map(x => DIMS[dims[0]].label(x)), cols: cols.map(x => DIMS[dims[1]].label(x)), values: vals, vmax: c.vmax };
      }
      return { type: "heat", rows: ms.map(m => m.name), cols: G.map(g => label(g, dims)), values: ms.map(m => G.map(g => g.ns[m.j] >= r.minN ? g.vals[m.j] : null)), vmax: c.vmax };
    }
    if (type === "pie") {
      if (!dims.length && ms.length > 1) return { type: "pie", cats: ms.map(m => m.name), series: [{ values: ms.map(m => G[0].vals[m.j]), colors: c.colors || null }] };
      return { type: "pie", cats: G.map(g => label(g, dims)), series: [{ values: G.map(g => g.vals[ms[0].j]), colors: c.colors || (dims[0] ? colorsFor(dims[0], G.map(g => g.k[0])) : null) }] };
    }
    if (type === "multi") return { type: "multi", cats: G.map(g => label(g, dims)), panels: ms.map((m, i) => ({ name: m.name, values: G.map(g => g.vals[m.j]), color: (c.colors || CAT)[i % CAT.length] })) };
    if (!dims.length && ms.length > 1 && (type === "hbar" || type === "bar")) {
      let items = ms.map((m, i) => ({ name: m.name, v: G[0].vals[m.j], col: c.colors ? c.colors[i] : "var(--c1)" }));
      if (c.sortDesc) items.sort((a, b) => b.v - a.v); if (c.top) items = items.slice(0, c.top);
      return { type, cats: items.map(x => x.name), series: [{ name: "", values: items.map(x => x.v), colors: items.map(x => x.col) }], fmt, labels: true, ymax: c.ymax, xmax: c.xmax };
    }
    let cats, series;
    if (dims.length === 2 && ms.length === 1) {
      const k1 = [...new Set(G.map(g => g.k[0]))], k2 = [...new Set(G.map(g => g.k[1]))];
      const byX = type === "line" ? k1 : k1; cats = byX.map(k => DIMS[dims[0]].label(k));
      const cs = colorsFor(dims[1], k2);
      series = k2.map((b, j) => ({ name: DIMS[dims[1]].label(b), color: cs[j], values: byX.map(a => { const g = G.find(x => x.k[0] === a && x.k[1] === b); return g ? g.vals[ms[0].j] : NaN; }) }));
    } else {
      cats = G.map(g => label(g, dims));
      const single = ms.length === 1, cs = dims[0] ? colorsFor(dims[0], G.map(g => g.k[0])) : null;
      series = ms.map((m, i) => ({ name: m.name, values: G.map(g => g.vals[m.j]), color: c.colors ? c.colors[i] : CAT[i], colors: single && type !== "line" && cs && !c.colors ? cs : null }));
    }
    return { type, cats, series, fmt, labels: c.labels !== false, ymax: c.ymax, ymin: c.ymin, zero: c.zero, endLabels: c.endLabels, yLabel: c.yLabel, height: c.height, nOf: dims.length < 2 ? G.map(g => g.n) : null, valueLabel: c.valueLabel };
  }

  /* ---------- kết quả -> bảng HTML */
  function toTable(r, maxRows = 80) {
    if (r.mode === "points") return `<p class="small" style="padding:10px">${fmtNum(r.points.length)} điểm (lấy mẫu từ ${fmtNum(r.n)} hộ).</p>`;
    if (r.mode === "hist") return `<p class="small" style="padding:10px">${fmtNum(r.n)} hộ · mean ${fmtNum(r.log ? Math.pow(10, r.mean) : r.mean, 1)} · median ${fmtNum(r.log ? Math.pow(10, r.median) : r.median, 1)}${r.log ? " (trung bình trên thang log)" : ""}</p>`;
    if (r.mode === "box") return `<table class="t"><tr><th>${esc(DIM_LABEL[r.dims[0]] || "Nhóm")}</th><th>n</th><th>q(0,1)</th><th>Q1</th><th>Median</th><th>Q3</th><th>q(0,9)</th><th>Mean</th></tr>${r.boxes.map(b => `<tr><td>${esc(b.k[0])}</td><td class="n">${fmtNum(b.n)}</td>${[b.lo, b.q1, b.med, b.q3, b.hi, b.mean].map(v => `<td class="n">${fmtNum(v, v < 10 ? 2 : 1)}</td>`).join("")}</tr>`).join("")}</table>`;
    const ms = r.measures.map((m, j) => ({ ...m, j })).filter(m => !m.hide);
    const head = `<tr>${r.dims.map(d => `<th>${esc(DIM_LABEL[d] || d)}</th>`).join("") || "<th>Nhóm</th>"}${ms.map(m => `<th>${esc(m.name)}</th>`).join("")}<th>n hộ</th></tr>`;
    const body = r.groups.slice(0, maxRows).map(g => `<tr>${r.dims.length ? g.k.slice(0, r.dims.length).map((k, j) => `<td>${esc(DIMS[r.dims[j]].label(k))}</td>`).join("") : "<td>Toàn quốc</td>"}${ms.map(m => { const v = g.vals[m.j]; const d = Math.abs(v) >= 100 ? 0 : Math.abs(v) >= 1 ? 1 : 3; return `<td class="n">${fmtNum(v, d)}${["pct", "share", "sumshare"].includes(m.agg) ? "%" : ""}</td>`; }).join("")}<td class="n"${g.n < r.minN ? ' style="color:var(--F-d)" title="dưới 30 hộ"' : ""}>${fmtNum(g.n)}</td></tr>`).join("");
    return `<table class="t">${head}${body}</table>`;
  }
  /* ---------- kết quả -> văn bản gửi Claude */
  function toText(r, maxRows = 70) {
    if (r.mode !== "group") return toTable(r).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
    const ms = r.measures.map((m, j) => ({ ...m, j })).filter(m => !m.hide);
    const lines = [[...(r.dims.length ? r.dims.map(d => DIM_LABEL[d] || d) : ["nhóm"]), ...ms.map(m => m.name + (["pct", "share", "sumshare"].includes(m.agg) ? " (%)" : "")), "n_hộ"].join(" | ")];
    r.groups.slice(0, maxRows).forEach(g => lines.push([...(r.dims.length ? g.k.slice(0, r.dims.length).map((k, j) => DIMS[r.dims[j]].label(k)) : ["Toàn quốc"]), ...ms.map(m => fmtNum(g.vals[m.j], Math.abs(g.vals[m.j]) >= 100 ? 0 : 2)), g.n].join(" | ")));
    if (r.groups.length > maxRows) lines.push(`… (${r.groups.length - maxRows} dòng nữa)`);
    if (r.small.length) lines.push("Nhóm dưới " + r.minN + " hộ (không nên kết luận): " + r.small.slice(0, 20).join(", "));
    return lines.join("\n");
  }

  return { N, V, S, VARS, DIMS, DIM_NOTE, AGGS, PROV, compile, run, toChart, toTable, toText, colorsFor, label, quant };
})();
