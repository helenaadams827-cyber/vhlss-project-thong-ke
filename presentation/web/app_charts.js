/* ============================================================
   Charts — bộ vẽ SVG nhỏ, màu lấy từ biến CSS (tự đổi theo theme)
   ============================================================ */
const CAT = ["var(--c1)", "var(--c2)", "var(--c3)", "var(--c4)", "var(--c5)", "var(--c6)", "var(--cslate)", "var(--cgray)"];
const ORD = ["var(--o1)", "var(--o2)", "var(--o3)", "var(--o4)"];

function fmtNum(v, d = 0) {
  if (v == null || !isFinite(v)) return "–";
  const s = Math.abs(v).toFixed(d).split(".");
  s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return (v < 0 ? "−" : "") + s.join(",");
}
function autoDec(vals) {
  const m = Math.max(...vals.filter(v => isFinite(v)).map(Math.abs), 0);
  return m >= 100 ? 0 : m >= 10 ? 1 : m >= 1 ? 1 : 2;
}
function makeFmt(kind, vals) {
  if (typeof kind === "function") return kind;
  if (kind === "pct") return v => fmtNum(v, Math.max(...vals.map(Math.abs)) >= 20 ? 0 : 1) + "%";
  if (kind === "pct1") return v => fmtNum(v, 1) + "%";
  if (kind === "r") return v => fmtNum(v, 2);
  if (typeof kind === "string" && /^num\d$/.test(kind)) { const d = +kind[3]; return v => fmtNum(v, d); }
  const d = autoDec(vals); return v => fmtNum(v, d);
}
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

function niceTicks(lo, hi, n = 5) {
  if (!(hi > lo)) { hi = lo + 1; }
  const span = hi - lo, step0 = span / n, mag = Math.pow(10, Math.floor(Math.log10(step0)));
  const err = step0 / mag, step = mag * (err >= 7.5 ? 10 : err >= 3.5 ? 5 : err >= 1.5 ? 2 : 1);
  const t0 = Math.floor(lo / step) * step, t1 = Math.ceil(hi / step) * step, out = [];
  for (let t = t0; t <= t1 + step * 1e-9; t += step) out.push(+t.toFixed(10));
  return out;
}

/* ---------- tooltip */
const Tip = {
  el: null,
  show(html, ev) { const t = this.el; t.innerHTML = html; t.style.opacity = 1; this.move(ev); },
  move(ev) {
    const t = this.el, pad = 14; let x = ev.clientX + pad, y = ev.clientY + pad;
    const w = t.offsetWidth, h = t.offsetHeight;
    if (x + w > innerWidth - 8) x = ev.clientX - w - pad;
    if (y + h > innerHeight - 8) y = ev.clientY - h - pad;
    t.style.left = x + "px"; t.style.top = y + "px";
  },
  hide() { this.el.style.opacity = 0; }
};
function wireTips(root) {
  root.querySelectorAll("[data-tip]").forEach(n => {
    n.addEventListener("mouseenter", e => Tip.show(n.getAttribute("data-tip"), e));
    n.addEventListener("mousemove", e => Tip.move(e));
    n.addEventListener("mouseleave", () => Tip.hide());
  });
}

/* ---------- khung chung */
const Charts = {
  observers: new WeakMap(),
  render(el, spec) {
    el._spec = spec;
    this.draw(el);
    if (!this.observers.has(el) && "ResizeObserver" in window) {
      let last = el.clientWidth, timer;
      const ro = new ResizeObserver(() => {
        if (Math.abs(el.clientWidth - last) < 8) return;
        last = el.clientWidth; clearTimeout(timer); timer = setTimeout(() => this.draw(el), 80);
      });
      ro.observe(el); this.observers.set(el, ro);
    }
  },
  draw(el) {
    const spec = el._spec; if (!spec) return;
    const W = Math.max(280, el.clientWidth || 600);
    const fn = this[spec.type] || this.bar;
    const svg = fn.call(this, spec, W);
    el.innerHTML = svg; wireTips(el);
  },
  svg(W, H, body, label) {
    return `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(label || "biểu đồ")}" style="font-family:var(--font)">${body}</svg>`;
  },
  legend(items, x, y, W) {
    let out = "", cx = x, cy = y;
    for (const it of items) {
      const w = 18 + it.name.length * 6.6;
      if (cx + w > W - 4 && cx > x) { cx = x; cy += 18; }
      out += `<rect x="${cx}" y="${cy - 9}" width="10" height="10" rx="3" style="fill:${it.color}"/><text x="${cx + 14}" y="${cy}" font-size="12" style="fill:var(--ink2)">${esc(it.name)}</text>`;
      cx += w + 10;
    }
    return { svg: out, h: cy - y + 16 };
  },
  yAxis(ticks, sy, x0, x1, fmt) {
    return ticks.map(t => `<line x1="${x0}" x2="${x1}" y1="${sy(t)}" y2="${sy(t)}" style="stroke:var(--grid)" stroke-width="1"/><text x="${x0 - 6}" y="${sy(t) + 4}" text-anchor="end" font-size="11" style="fill:var(--muted)">${esc(fmt(t))}</text>`).join("");
  },
  wrapLabel(s, maxChars) {
    const words = String(s).split(" "); const lines = []; let cur = "";
    for (const w of words) { if ((cur + " " + w).trim().length > maxChars && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }
    if (cur) lines.push(cur); return lines.slice(0, 3);
  },

  /* ---------- cột (đơn, nhóm, chồng) */
  bar(s, W) {
    const series = s.series, cats = s.cats, all = series.flatMap(x => x.values).filter(isFinite);
    const fmt = makeFmt(s.fmt, all), stacked = s.type === "stack";
    const leg = series.length > 1 ? this.legend(series.map((x, i) => ({ name: x.name, color: x.color || CAT[i] })), 44, 14, W) : { svg: "", h: 0 };
    const H = s.height || Math.round(Math.min(380, Math.max(230, W * 0.46))) + leg.h;
    const maxLab = Math.max(...cats.map(c => String(c).length));
    const rot = cats.length > 10 && maxLab > 4;
    const m = { l: 46, r: 12, t: 12 + leg.h, b: rot ? 70 : (cats.some(c => String(c).length > 9) ? 40 : 28) };
    let hi = stacked ? 100 : Math.max(0, ...all), lo = stacked ? 0 : Math.min(0, ...all);
    if (s.ymax != null) hi = s.ymax; if (s.ymin != null) lo = s.ymin;
    const ticks = niceTicks(lo, hi * (stacked ? 1 : 1.08)); hi = ticks[ticks.length - 1]; lo = ticks[0];
    const pw = W - m.l - m.r, ph = H - m.t - m.b, sy = v => m.t + ph - (v - lo) / (hi - lo) * ph;
    const band = pw / cats.length, gw = band * (cats.length > 12 ? 0.8 : 0.7);
    const bw = stacked ? gw : gw / series.length;
    let body = this.yAxis(ticks, sy, m.l, W - m.r, fmt), labels = "";
    const showLab = s.labels !== false && cats.length * (stacked ? 1 : series.length) <= 28;
    cats.forEach((c, i) => {
      const gx = m.l + band * i + (band - gw) / 2; let acc = 0;
      series.forEach((sr, j) => {
        const v = sr.values[i]; if (!isFinite(v)) return;
        const col = (sr.colors && sr.colors[i]) || sr.color || CAT[j];
        let x, y0, y1;
        if (stacked) { x = gx; y0 = sy(acc + v); y1 = sy(acc); acc += v; }
        else { x = gx + bw * j; y0 = sy(Math.max(v, 0)); y1 = sy(Math.min(v, 0)); }
        const h = Math.max(0.5, y1 - y0), w = Math.max(1, (stacked ? gw : bw) - 2);
        const tip = `<b>${esc(c)}</b>${series.length > 1 ? " · " + esc(sr.name) : ""}<br>${esc(fmt(v))}${s.nOf ? `<br><span style="opacity:.75">n = ${fmtNum(s.nOf[i])}</span>` : ""}`;
        body += `<rect x="${x + 1}" y="${y0}" width="${w}" height="${h}" rx="${Math.min(4, w / 3)}" style="fill:${col}" data-tip="${esc(tip)}"/>`;
        if (showLab) {
          if (stacked) { if (h > 14) labels += `<text x="${x + w / 2 + 1}" y="${y0 + h / 2 + 4}" text-anchor="middle" font-size="11" style="fill:var(--ink)">${esc(fmt(v))}</text>`; }
          else if (w >= 16) labels += `<text x="${x + w / 2 + 1}" y="${(v >= 0 ? y0 - 4 : y1 + 12)}" text-anchor="middle" font-size="${w < 26 ? 10 : 11}" style="fill:var(--ink2)">${esc(fmt(v))}</text>`;
        }
      });
      const lx = m.l + band * i + band / 2;
      if (rot) body += `<text transform="translate(${lx + 3},${m.t + ph + 8}) rotate(-50)" text-anchor="end" font-size="11" style="fill:var(--ink2)">${esc(c)}</text>`;
      else this.wrapLabel(c, Math.max(6, Math.floor(band / 7))).forEach((ln, k) => body += `<text x="${lx}" y="${m.t + ph + 16 + k * 13}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(ln)}</text>`);
    });
    body += `<line x1="${m.l}" x2="${W - m.r}" y1="${sy(0 < lo ? lo : 0)}" y2="${sy(0 < lo ? lo : 0)}" style="stroke:var(--axis)"/>`;
    if (s.yLabel) body += `<text x="${m.l}" y="${m.t - 4 - (leg.h ? 0 : 0)}" font-size="11" style="fill:var(--muted)"></text>`;
    return this.svg(W, H, leg.svg + body + labels + (s.yLabel ? `<text x="4" y="${m.t + ph / 2}" font-size="11" transform="rotate(-90 10 ${m.t + ph / 2})" text-anchor="middle" style="fill:var(--muted)">${esc(s.yLabel)}</text>` : ""), s.title);
  },
  stack(s, W) { return this.bar(s, W); },

  /* ---------- thanh ngang (nhóm, hai chiều) */
  hbar(s, W) {
    const series = s.series, cats = s.cats, all = series.flatMap(x => x.values).filter(isFinite);
    const fmt = makeFmt(s.fmt, all);
    const leg = series.length > 1 ? this.legend(series.map((x, i) => ({ name: x.name, color: x.color || CAT[i] })), 8, 14, W) : { svg: "", h: 0 };
    const rowH = series.length > 1 ? 14 * series.length + 10 : 24;
    const labW = Math.min(W * 0.36, 8 + 6.6 * Math.max(...cats.map(c => String(c).length)));
    const m = { l: labW + 10, r: 64, t: 8 + leg.h, b: 8 };
    const H = m.t + m.b + rowH * cats.length;
    let lo = Math.min(0, ...all), hi = Math.max(0, ...all); if (s.xmax != null) hi = s.xmax;
    const negPad = lo < 0 ? 40 : 0;
    const pw = W - m.l - m.r - negPad, sx = v => m.l + negPad + (v - lo) / (hi - lo || 1) * pw;
    let body = "";
    cats.forEach((c, i) => {
      const y = m.t + rowH * i;
      body += `<text x="${m.l - 8}" y="${y + rowH / 2 + 4}" text-anchor="end" font-size="12" style="fill:var(--ink2)">${esc(c)}</text>`;
      series.forEach((sr, j) => {
        const v = sr.values[i]; if (!isFinite(v)) return;
        const col = (sr.colors && sr.colors[i]) || sr.color || CAT[j];
        const bh = series.length > 1 ? 12 : 16, yy = y + (rowH - bh * series.length) / 2 + bh * j;
        const x0 = sx(Math.min(0, v)), x1 = sx(Math.max(0, v));
        const tip = `<b>${esc(c)}</b>${series.length > 1 ? " · " + esc(sr.name) : ""}<br>${esc(fmt(v))}${s.nOf ? `<br><span style="opacity:.75">n = ${fmtNum(s.nOf[i])}</span>` : ""}`;
        body += `<rect x="${x0}" y="${yy + 1}" width="${Math.max(1, x1 - x0)}" height="${bh - 2}" rx="3" style="fill:${col}" data-tip="${esc(tip)}"/>`;
        const lab = (s.valueLabel ? s.valueLabel(v, i, j) : fmt(v));
        body += `<text x="${v >= 0 ? x1 + 5 : x0 - 5}" y="${yy + bh / 2 + 3.5}" text-anchor="${v >= 0 ? "start" : "end"}" font-size="11" style="fill:var(--ink2)">${esc(lab)}</text>`;
      });
    });
    if (lo < 0) body += `<line x1="${sx(0)}" x2="${sx(0)}" y1="${m.t}" y2="${H - m.b}" style="stroke:var(--axis)"/>`;
    return this.svg(W, H, leg.svg + body, s.title);
  },

  /* ---------- đường */
  line(s, W) {
    const series = s.series, cats = s.cats, all = series.flatMap(x => x.values).filter(isFinite);
    const fmt = makeFmt(s.fmt, all);
    const leg = series.length > 1 && !s.endLabels ? this.legend(series.map((x, i) => ({ name: x.name, color: x.color || CAT[i] })), 46, 14, W) : { svg: "", h: 0 };
    const H = s.height || Math.round(Math.min(340, Math.max(220, W * 0.42))) + leg.h;
    const m = { l: 46, r: s.endLabels ? (s.endLabels === "path" ? 150 : 96) : 18, t: 14 + leg.h, b: 30 };
    let lo = Math.min(...all), hi = Math.max(...all);
    if (s.ymin != null) lo = s.ymin; else if (s.zero) lo = Math.min(0, lo);
    const pad = (hi - lo) * 0.12 || 1; let lo2 = s.ymin != null ? lo : lo - pad; if (lo >= 0 && lo2 < 0) lo2 = 0; const ticks = niceTicks(lo2, hi + pad);
    lo = ticks[0]; hi = ticks[ticks.length - 1];
    const pw = W - m.l - m.r, ph = H - m.t - m.b;
    const sx = i => m.l + (cats.length === 1 ? pw / 2 : pw * i / (cats.length - 1)), sy = s.invert ? (v => m.t + (v - lo) / (hi - lo) * ph) : (v => m.t + ph - (v - lo) / (hi - lo) * ph);
    let body = this.yAxis(ticks, sy, m.l, W - m.r, fmt);
    cats.forEach((c, i) => body += `<text x="${sx(i)}" y="${H - 10}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(c)}</text>`);
    const ends = [];
    series.forEach((sr, j) => {
      const col = sr.color || CAT[j]; let d = "";
      sr.values.forEach((v, i) => { if (isFinite(v)) d += (d ? "L" : "M") + sx(i) + " " + sy(v); });
      body += `<path d="${d}" fill="none" style="stroke:${col}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>`;
      sr.values.forEach((v, i) => { if (isFinite(v)) body += `<circle cx="${sx(i)}" cy="${sy(v)}" r="4.5" style="fill:${col};stroke:var(--surface)" stroke-width="1.5" data-tip="${esc(`<b>${esc(sr.name || "")}</b> · ${esc(cats[i])}<br>${esc(fmt(v))}`)}"/>`; });
      const last = sr.values.length - 1;
      if (s.endLabels && isFinite(sr.values[last])) {
        let txt = sr.name + " " + fmt(sr.values[last]);
        if (s.endLabels === "change" && isFinite(sr.values[0]) && sr.values[0]) txt = sr.name + " " + (sr.values[last] >= sr.values[0] ? "+" : "−") + fmtNum(Math.abs(sr.values[last] / sr.values[0] - 1) * 100, 0) + "%";
        if (s.endLabels === "path") txt = sr.name + " " + sr.values.map(v => fmtNum(v, 0)).join("→");
        ends.push({ y: sy(sr.values[last]), txt, col });
      }
    });
    ends.sort((a, b) => a.y - b.y); for (let k = 1; k < ends.length; k++) ends[k].y = Math.max(ends[k].y, ends[k - 1].y + 14);
    ends.forEach(e => body += `<text x="${W - m.r + 8}" y="${e.y + 4}" font-size="11.5" style="fill:var(--ink2)"><tspan style="fill:${e.col}">●</tspan> ${esc(e.txt)}</text>`);
    return this.svg(W, H, leg.svg + body, s.title);
  },

  /* ---------- điểm đầu -> điểm cuối (dumbbell) */
  dumbbell(s, W) {
    const cats = s.cats, a = s.from, b = s.to, all = a.concat(b).filter(isFinite), fmt = makeFmt(s.fmt, all);
    const order = cats.map((c, i) => i).sort((i, j) => (b[j] - a[j]) - (b[i] - a[i]));
    const labW = Math.min(W * 0.34, 8 + 6.8 * Math.max(...cats.map(c => String(c).length)));
    const m = { l: labW + 10, r: 58, t: 30, b: 8 }, rowH = 24, H = m.t + m.b + rowH * cats.length;
    const hi = Math.max(...all) * 1.04, lo = Math.min(0, ...all), pw = W - m.l - m.r, sx = v => m.l + (v - lo) / (hi - lo) * pw;
    let body = `<text x="${m.l}" y="14" font-size="11.5" style="fill:var(--ink2)"><tspan style="fill:var(--cgray)">●</tspan> ${esc(s.fromLabel || "đầu")}  →  <tspan style="fill:var(--c1)">▶</tspan> ${esc(s.toLabel || "cuối")} (tăng)   <tspan style="fill:var(--c2)">▶</tspan> giảm</text>`;
    niceTicks(lo, hi, 5).filter(t => t <= hi).forEach(t => body += `<line x1="${sx(t)}" x2="${sx(t)}" y1="${m.t - 6}" y2="${H - m.b}" style="stroke:var(--grid)"/>`);
    order.forEach((i, k) => {
      const y = m.t + rowH * k + rowH / 2, up = b[i] >= a[i], col = up ? "var(--c1)" : "var(--c2)", x0 = sx(a[i]), x1 = sx(b[i]);
      const tip = `<b>${esc(cats[i])}</b><br>${esc(s.fromLabel || "")}: ${esc(fmt(a[i]))}<br>${esc(s.toLabel || "")}: ${esc(fmt(b[i]))}<br>thay đổi: ${up ? "+" : "−"}${fmtNum(Math.abs(b[i] - a[i]), 1)} ${esc(s.unit || "")}`;
      body += `<text x="${m.l - 8}" y="${y + 4}" text-anchor="end" font-size="12" style="fill:var(--ink2)">${esc(cats[i])}</text>`;
      body += `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" style="stroke:${col}" stroke-width="3" stroke-linecap="round"/>`;
      body += `<circle cx="${x0}" cy="${y}" r="4.5" style="fill:var(--cgray)"/>`;
      const dir = up ? 1 : -1; body += `<path d="M${x1} ${y} l${-7 * dir} -5 l0 10 z" style="fill:${col}" data-tip="${esc(tip)}"/>`;
      body += `<rect x="${Math.min(x0, x1) - 6}" y="${y - 10}" width="${Math.abs(x1 - x0) + 12}" height="20" fill="transparent" data-tip="${esc(tip)}"/>`;
      body += `<text x="${Math.max(x0, x1) + 8}" y="${y + 4}" font-size="11" style="fill:var(--ink2)">${up ? "+" : "−"}${fmtNum(Math.abs(b[i] - a[i]), 1)}</text>`;
    });
    return this.svg(W, H, body, s.title);
  },

  /* ---------- tròn (donut) */
  pie(s, W) {
    const vals = s.series[0].values, cats = s.cats, tot = vals.reduce((a, b) => a + (isFinite(b) ? b : 0), 0);
    const H = s.height || 240, R = Math.min(H / 2 - 12, W * 0.22), cx = Math.min(W * 0.3, R + 20), cy = H / 2;
    let a0 = -Math.PI / 2, body = "";
    vals.forEach((v, i) => {
      if (!(v > 0)) return; const a1 = a0 + v / tot * Math.PI * 2, big = a1 - a0 > Math.PI ? 1 : 0, r0 = R * 0.56;
      const p = (a, r) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
      const [x0, y0] = p(a0, R), [x1, y1] = p(a1, R), [x2, y2] = p(a1, r0), [x3, y3] = p(a0, r0);
      const col = (s.series[0].colors && s.series[0].colors[i]) || CAT[i % CAT.length];
      body += `<path d="M${x0} ${y0}A${R} ${R} 0 ${big} 1 ${x1} ${y1}L${x2} ${y2}A${r0} ${r0} 0 ${big} 0 ${x3} ${y3}Z" style="fill:${col};stroke:var(--surface)" stroke-width="2" data-tip="${esc(`<b>${esc(cats[i])}</b><br>${fmtNum(v / tot * 100, 1)}%`)}"/>`;
      a0 = a1;
    });
    let ly = cy - cats.length * 11 + 6;
    cats.forEach((c, i) => {
      const col = (s.series[0].colors && s.series[0].colors[i]) || CAT[i % CAT.length];
      body += `<rect x="${cx + R + 24}" y="${ly - 9}" width="10" height="10" rx="3" style="fill:${col}"/><text x="${cx + R + 40}" y="${ly}" font-size="12.5" style="fill:var(--ink2)">${esc(c)} <tspan style="fill:var(--ink)" font-weight="600">${fmtNum(vals[i] / tot * 100, 1)}%</tspan></text>`;
      ly += 22;
    });
    return this.svg(W, H, body, s.title);
  },

  /* ---------- phân tán / bong bóng */
  scatter(s, W) {
    const pts = s.points.filter(p => isFinite(p.x) && isFinite(p.y));
    const H = s.height || Math.round(Math.min(400, Math.max(250, W * 0.5)));
    const m = { l: 52, r: 16, t: 14, b: 40 };
    const tx = v => s.logx ? Math.log10(v) : v, ty = v => s.logy ? Math.log10(v) : v;
    const P = pts.filter(p => (!s.logx || p.x > 0) && (!s.logy || p.y > 0));
    let x0 = Math.min(...P.map(p => tx(p.x))), x1 = Math.max(...P.map(p => tx(p.x))), y0 = Math.min(...P.map(p => ty(p.y))), y1 = Math.max(...P.map(p => ty(p.y)));
    if (s.ymin != null) y0 = ty(s.ymin); if (s.ymax != null) y1 = ty(s.ymax);
    const px = (x1 - x0) * 0.06 || 1, py = (y1 - y0) * 0.08 || 1; x0 -= px; x1 += px; y0 -= s.ymin != null ? 0 : py; y1 += py;
    const pw = W - m.l - m.r, ph = H - m.t - m.b, sx = v => m.l + (tx(v) - x0) / (x1 - x0) * pw, sy = v => m.t + ph - (ty(v) - y0) / (y1 - y0) * ph;
    const logf = v => v >= 1 ? fmtNum(v, 0) : fmtNum(v, v >= 0.1 ? 1 : 2);
    const fx = s.logx ? logf : makeFmt(s.fmtx, P.map(p => p.x)), fy = s.logy ? logf : makeFmt(s.fmty, P.map(p => p.y));
    const tk = (a, b, log) => log ? niceTicks(a, b, 4).filter(t => Number.isInteger(t)).map(t => Math.pow(10, t)) : niceTicks(a, b, 5);
    let body = "";
    tk(y0, y1, s.logy).forEach(t => { const y = sy(t); if (y >= m.t - 1 && y <= m.t + ph + 1) body += `<line x1="${m.l}" x2="${W - m.r}" y1="${y}" y2="${y}" style="stroke:var(--grid)"/><text x="${m.l - 6}" y="${y + 4}" text-anchor="end" font-size="11" style="fill:var(--muted)">${esc(fy(t))}</text>`; });
    tk(x0, x1, s.logx).forEach(t => { const x = sx(t); if (x >= m.l - 1 && x <= W - m.r + 1) body += `<line x1="${x}" x2="${x}" y1="${m.t}" y2="${m.t + ph}" style="stroke:var(--grid)"/><text x="${x}" y="${H - 22}" text-anchor="middle" font-size="11" style="fill:var(--muted)">${esc(fx(t))}</text>`; });
    if (s.xLabel) body += `<text x="${m.l + pw / 2}" y="${H - 4}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(s.xLabel)}</text>`;
    if (s.yLabel) body += `<text x="12" y="${m.t + ph / 2}" transform="rotate(-90 12 ${m.t + ph / 2})" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(s.yLabel)}</text>`;
    const small = P.length > 400;
    P.forEach(p => {
      const r = p.r || (small ? 1.8 : 4.5);
      body += `<circle cx="${sx(p.x)}" cy="${sy(p.y)}" r="${r}" style="fill:${p.color || "var(--c1)"};${small ? "opacity:.28" : "opacity:.85;stroke:var(--surface)"}" stroke-width="${small ? 0 : 1}"${p.tip ? ` data-tip="${esc(p.tip)}"` : ""}/>`;
      if (p.label) body += `<text x="${sx(p.x) + r + 3}" y="${sy(p.y) + 4}" font-size="11" style="fill:var(--ink2)">${esc(p.label)}</text>`;
    });
    let leg = "";
    if (s.legend) leg = this.legend(s.legend, m.l + 6, m.t + 12, W).svg;
    if (s.note) body += `<text x="${W - m.r - 4}" y="${m.t + ph - 6}" text-anchor="end" font-size="11" style="fill:var(--muted)">${esc(s.note)}</text>`;
    return this.svg(W, H, body + leg, s.title);
  },

  /* ---------- hộp */
  box(s, W) {
    const b = s.boxes, H = s.height || 260, m = { l: 52, r: 14, t: 14, b: 30 };
    const T = v => s.log ? Math.log10(v) : v;
    let lo = Math.min(...b.map(x => T(Math.max(x.lo, s.log ? 1e-9 : -Infinity)))), hi = Math.max(...b.map(x => T(x.hi)));
    const pad = (hi - lo) * 0.06; lo -= pad; hi += pad;
    const pw = W - m.l - m.r, ph = H - m.t - m.b, sy = v => m.t + ph - (T(v) - lo) / (hi - lo) * ph;
    const fmt = makeFmt(s.fmt, b.map(x => x.med));
    let ticks = s.log ? niceTicks(lo, hi, 4).filter(t => Number.isInteger(t)).map(t => Math.pow(10, t)) : niceTicks(lo, hi);
    ticks = ticks.filter(t => sy(t) >= m.t - 1 && sy(t) <= m.t + ph + 1);
    let body = this.yAxis(ticks, sy, m.l, W - m.r, fmt);
    const band = pw / b.length, bw = Math.min(46, band * 0.5);
    b.forEach((x, i) => {
      const cx = m.l + band * i + band / 2, col = x.color || CAT[0];
      const tip = `<b>${esc(x.cat)}</b><br>q(0,1) ${fmt(x.lo)} · Q1 ${fmt(x.q1)}<br>median ${fmt(x.med)} · Q3 ${fmt(x.q3)}<br>q(0,9) ${fmt(x.hi)}${x.mean != null ? "<br>mean " + fmt(x.mean) : ""}<br>n = ${fmtNum(x.n)}`;
      body += `<line x1="${cx}" x2="${cx}" y1="${sy(x.hi)}" y2="${sy(x.lo)}" style="stroke:var(--ink2)" stroke-width="1.2"/>`;
      body += `<rect x="${cx - bw / 2}" y="${sy(x.q3)}" width="${bw}" height="${Math.max(1, sy(x.q1) - sy(x.q3))}" rx="4" style="fill:${col}" data-tip="${esc(tip)}"/>`;
      body += `<line x1="${cx - bw / 2}" x2="${cx + bw / 2}" y1="${sy(x.med)}" y2="${sy(x.med)}" style="stroke:var(--surface)" stroke-width="2.5"/>`;
      if (x.mean != null) body += `<circle cx="${cx}" cy="${sy(x.mean)}" r="3.2" style="fill:var(--surface);stroke:var(--ink)" stroke-width="1.2"/>`;
      body += `<text x="${cx}" y="${H - 10}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(x.cat)}</text>`;
    });
    body += `<text x="${W - m.r}" y="${m.t + 4}" text-anchor="end" font-size="11" style="fill:var(--muted)">hộp: Q1–Q3 · vạch: q(0,1)–q(0,9) · ○ mean</text>`;
    return this.svg(W, H, body, s.title);
  },

  /* ---------- histogram */
  hist(s, W) {
    const bins = s.bins, H = s.height || 240, m = { l: 48, r: 12, t: 12, b: 34 };
    const hi = Math.max(...bins.map(b => b.n)), ticks = niceTicks(0, hi * 1.05);
    const pw = W - m.l - m.r, ph = H - m.t - m.b, sy = v => m.t + ph - v / ticks[ticks.length - 1] * ph;
    const x0 = bins[0].x0, x1 = bins[bins.length - 1].x1, sx = v => m.l + (v - x0) / (x1 - x0) * pw;
    let body = this.yAxis(ticks, sy, m.l, W - m.r, v => fmtNum(v));
    bins.forEach(b => body += `<rect x="${sx(b.x0) + 0.5}" y="${sy(b.n)}" width="${Math.max(1, sx(b.x1) - sx(b.x0) - 1)}" height="${m.t + ph - sy(b.n)}" style="fill:${s.color || "var(--c1)"}" data-tip="${esc(`${esc(s.binLabel ? s.binLabel(b) : fmtNum(b.x0, 1) + "–" + fmtNum(b.x1, 1))}<br>${fmtNum(b.n)} hộ`)}"/>`);
    const tk = niceTicks(x0, x1, 6).filter(t => t >= x0 && t <= x1);
    tk.forEach(t => body += `<text x="${sx(t)}" y="${H - 18}" text-anchor="middle" font-size="11" style="fill:var(--muted)">${esc(s.tickLabel ? s.tickLabel(t) : fmtNum(t, 0))}</text>`);
    if (s.xLabel) body += `<text x="${m.l + pw / 2}" y="${H - 3}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(s.xLabel)}</text>`;
    (s.marks || []).forEach(k => body += `<line x1="${sx(k.x)}" x2="${sx(k.x)}" y1="${m.t}" y2="${m.t + ph}" style="stroke:var(--ink)" stroke-dasharray="3 3"/><text x="${sx(k.x) + 4}" y="${m.t + 12 + (k.dy || 0)}" font-size="11" style="fill:var(--ink)">${esc(k.label)}</text>`);
    return this.svg(W, H, body, s.title);
  },

  /* ---------- heatmap (bảng tương quan tô màu) */
  heat(s, W) {
    const rows = s.rows, cols = s.cols, V = s.values;
    const labW = Math.min(170, 8 + 6.8 * Math.max(...rows.map(r => r.length)));
    const extra = s.extra ? 58 : 0;
    const cw = Math.max(34, (W - labW - extra - 8) / cols.length), ch = 26, top = 44;
    const H = top + ch * rows.length + 6;
    const vmax = s.vmax || 0.65;
    let body = "";
    cols.forEach((c, j) => this.wrapLabel(c, Math.max(4, Math.floor(cw / 7))).forEach((ln, k, arr) => body += `<text x="${labW + cw * j + cw / 2}" y="${top - 8 - (arr.length - 1 - k) * 13}" text-anchor="middle" font-size="11" style="fill:var(--ink2)">${esc(ln)}</text>`));
    if (s.extra) body += `<text x="${labW + cw * cols.length + extra / 2}" y="${top - 8}" text-anchor="middle" font-size="11" style="fill:var(--ink2)">${esc(s.extra.name)}</text>`;
    rows.forEach((r, i) => {
      const y = top + ch * i;
      body += `<text x="${labW - 8}" y="${y + ch / 2 + 4}" text-anchor="end" font-size="12" style="fill:var(--ink2)">${esc(r)}</text>`;
      cols.forEach((c, j) => {
        const v = V[i][j], x = labW + cw * j, ok = v != null && isFinite(v);
        const t = ok ? Math.max(0, Math.min(1, v / vmax)) : 0;
        const fill = ok ? `color-mix(in srgb, var(--o4) ${Math.round(t * 100)}%, var(--surface2))` : "var(--surface2)";
        body += `<rect x="${x + 1}" y="${y + 1}" width="${cw - 2}" height="${ch - 2}" rx="4" style="fill:${fill}" data-tip="${esc(`<b>${esc(r)}</b> · ${esc(c)}<br>r = ${ok ? fmtNum(v, 2) : "ít hơn 30 hộ"}`)}"/>`;
        body += `<text x="${x + cw / 2}" y="${y + ch / 2 + 4}" text-anchor="middle" font-size="11" style="fill:${ok ? (t > 0.72 ? "var(--surface)" : "var(--ink)") : "var(--muted)"}">${ok ? fmtNum(v, 2) : "–"}</text>`;
      });
      if (s.extra) body += `<text x="${labW + cw * cols.length + extra / 2}" y="${y + ch / 2 + 4}" text-anchor="middle" font-size="11.5" style="fill:var(--ink2)">${esc(s.extra.values[i])}</text>`;
    });
    return this.svg(W, H, body, s.title);
  },

  /* ---------- nhiều biểu đồ nhỏ (small multiples) */
  multi(s, W) {
    const n = s.panels.length, cols = W < 520 ? 2 : Math.min(n, 3), pw = (W - (cols - 1) * 14) / cols;
    const rows = Math.ceil(n / cols), ph = 130, H = rows * (ph + 26);
    let body = "";
    s.panels.forEach((p, k) => {
      const ox = (k % cols) * (pw + 14), oy = Math.floor(k / cols) * (ph + 26);
      const v = p.values, lo = Math.min(...v), hi = Math.max(...v), pad = (hi - lo) * 0.5 + 0.5;
      const sx = i => ox + 16 + (pw - 60) * i / (v.length - 1), sy = x => oy + 30 + (ph - 50) * (1 - (x - (lo - pad)) / (hi - lo + 2 * pad));
      body += `<text x="${ox}" y="${oy + 14}" font-size="12" font-weight="600" style="fill:var(--ink)">${esc(p.name)}</text>`;
      body += `<line x1="${ox}" x2="${ox + pw}" y1="${oy + ph - 14}" y2="${oy + ph - 14}" style="stroke:var(--grid)"/>`;
      let d = ""; v.forEach((x, i) => d += (i ? "L" : "M") + sx(i) + " " + sy(x));
      body += `<path d="${d}" fill="none" style="stroke:${p.color || "var(--c1)"}" stroke-width="2.4" stroke-linecap="round"/>`;
      v.forEach((x, i) => {
        body += `<circle cx="${sx(i)}" cy="${sy(x)}" r="4" style="fill:${p.color || "var(--c1)"};stroke:var(--surface)" stroke-width="1.5" data-tip="${esc(`<b>${esc(p.name)}</b> · ${esc(s.cats[i])}<br>${fmtNum(x, 1)}`)}"/>`;
        body += `<text x="${sx(i)}" y="${oy + ph}" text-anchor="middle" font-size="10.5" style="fill:var(--muted)">${esc(s.cats[i])}</text>`;
      });
      body += `<text x="${sx(0)}" y="${sy(v[0]) - 8}" text-anchor="middle" font-size="11" style="fill:var(--ink2)">${fmtNum(v[0], v[0] < 10 ? 1 : 0)}</text>`;
      body += `<text x="${sx(v.length - 1)}" y="${sy(v[v.length - 1]) - 8}" text-anchor="middle" font-size="11" font-weight="600" style="fill:var(--ink)">${fmtNum(v[v.length - 1], v[v.length - 1] < 10 ? 1 : 0)}</text>`;
    });
    return this.svg(W, H, body, s.title);
  },
};
