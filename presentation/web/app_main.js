/* ============================================================
   Main — dựng trang, thẻ phân tích, hỏi dữ liệu, tự khám phá
   ============================================================ */
Tip.el = document.getElementById("tip");
const $ = (s, r = document) => r.querySelector(s);
const h = (html) => { const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstElementChild; };
const VERD = { U: "Ủng hộ", M: "Một phần", B: "Bác bỏ" };
const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) { } } };

/* ---------- báo lỗi khi mở với #debug */
if (location.hash.includes("debug")) {
  const box = h('<pre style="position:fixed;left:8px;bottom:8px;z-index:99;max-width:60vw;max-height:40vh;overflow:auto;background:#fff3f3;color:#900;font-size:11px;padding:8px;border-radius:8px" id="dbg"></pre>');
  document.body.append(box);
  window.addEventListener("error", e => box.textContent += e.message + " @" + e.lineno + "\n");
}

/* ---------- giao diện sáng / tối */
(function theme() {
  const modes = ["system", "light", "dark"], names = { system: "Theo máy", light: "Sáng", dark: "Tối" };
  let m = store.get("theme") || "system";
  const apply = () => { if (m === "system") document.documentElement.removeAttribute("data-theme"); else document.documentElement.setAttribute("data-theme", m); $("#themeBtn").textContent = "Giao diện: " + names[m]; };
  apply();
  $("#themeBtn").addEventListener("click", () => { m = modes[(modes.indexOf(m) + 1) % 3]; store.set("theme", m); apply(); });
})();

/* ---------- mở đầu */
Charts.render($("#heroChart"), Eng.toChart(Eng.run({ filter: "year==2014", groupBy: ["Q"], measures: [{ name: "Median thu nhập/người (triệu)", agg: "median", expr: "inc_head/1000" }] }), { type: "bar", fmt: "num1", height: 190 }));
$("#msgs").append(...MESSAGES.map(m => h(`<div class="msg st-${m.st}"><div class="k">${m.k}</div><p>${m.t}</p></div>`)));
$("#limits").append(...LIMITS.map(t => h(`<li>${t}</li>`)));
$("#knowledge").innerHTML = `<table class="t"><tr><th>Chương</th><th>Nội dung</th><th>Ở đâu</th></tr>${KNOWLEDGE.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join("")}</table>`;

/* ---------- thẻ phân tích */
function subst(q, P) { return JSON.parse(JSON.stringify(q).replace(/\$\{(\w+)\}/g, (_, k) => P[k])); }
function tiersHtml() {
  const by = { T1: [], T2: [], T3: [], T4: [] }; Eng.PROV.forEach(p => by[p.tier].push(p.name));
  const lab = { T1: "T1 · nghèo nhất", T2: "T2", T3: "T3", T4: "T4 · giàu nhất" };
  return `<div class="tiers">${Object.keys(by).map((t, i) => `<div class="tier" style="background:color-mix(in srgb, var(--o${i + 1}) 22%, var(--surface))"><b>${lab[t]} (${by[t].length} tỉnh)</b><span>${by[t].join(", ")}</span></div>`).join("")}</div>`;
}
let SAMPLE = null;
function renderCard(card, host) {
  const st = card.st || "N";
  const P = {}; (card.params || []).forEach(p => P[p.key] = p.def);
  const el = h(`<article class="card st-${st}${card.wide ? " wide" : ""}">
    <div class="card-top"><span class="code">${card.code}</span><h3>${card.title}</h3></div>
    <div class="hyp">${card.v ? `<span>Giả thuyết: ${card.hyp}</span><span class="verdict v-${card.v}">${VERD[card.v]}</span>` : `<span>Câu hỏi: ${card.hyp}</span>`}</div>
    <div class="ctrls"></div><div class="chart"></div><div class="extra"></div>
    <div class="notes">${card.notes.map(n => `<div class="note">${n}</div>`).join("")}</div>
    <div class="card-actions"></div><div class="ai-box" hidden></div><div class="tbl-wrap tbl" hidden></div>
    <div class="meta"><span><b>Thước đo</b> ${card.meta[0]}</span><span><b>Biểu đồ</b> ${card.meta[1]}</span><span><b>Kiến thức</b> ${card.meta[2]}</span></div></article>`);
  host.append(el);
  const chartEl = $(".chart", el), ctrls = $(".ctrls", el), tbl = $(".tbl", el), aiBox = $(".ai-box", el), acts = $(".card-actions", el);
  if (card.html) $(".extra", el).innerHTML = card.html;
  if (card.htmlAfter === "tiers") $(".extra", el).innerHTML = tiersHtml();
  if (!card.views) { chartEl.remove(); return; }
  let vi = 0, last = null;
  const seg = (items, cur, on, label) => {
    const s = h(`<div class="seg" role="group" aria-label="${label}"></div>`);
    items.forEach(([v, t], i) => { const b = h(`<button type="button" aria-pressed="${i === cur}">${t}</button>`); b.onclick = () => { [...s.children].forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); on(v); }; s.append(b); });
    return s;
  };
  if (card.views.length > 1) ctrls.append(seg(card.views.map((v, i) => [i, v.label]), 0, i => { vi = i; draw(); }, "Chọn cách xem"));
  (card.params || []).forEach(p => ctrls.append(seg(p.options, p.options.findIndex(o => o[0] === p.def), v => { P[p.key] = v; draw(); }, p.label)));
  function draw() {
    const v = card.views[vi];
    try {
      if (v.static) { Charts.render(chartEl, v.static); last = null; tbl.innerHTML = ""; return; }
      const r = Eng.run(subst(v.q, P)); last = r;
      Charts.render(chartEl, Eng.toChart(r, v.c || {}));
      if (!tbl.hidden) tbl.innerHTML = Eng.toTable(r);
    } catch (e) { chartEl.innerHTML = `<p class="small">Không vẽ được biểu đồ: ${esc(e.message)}</p>`; }
  }
  const tb = h(`<button class="linkbtn" type="button">Xem bảng số</button>`);
  tb.onclick = () => { tbl.hidden = !tbl.hidden; tb.textContent = tbl.hidden ? "Xem bảng số" : "Ẩn bảng số"; if (!tbl.hidden) tbl.innerHTML = last ? Eng.toTable(last) : "<p class='small' style='padding:10px'>Biểu đồ này dùng số đã tính sẵn.</p>"; };
  acts.append(tb);
  const ab = h(`<button class="linkbtn ask-card" type="button" hidden>Hỏi Claude về biểu đồ này</button>`);
  ab.onclick = async () => {
    if (!last || !SAMPLE) return; aiBox.hidden = false; aiBox.textContent = "Claude đang đọc bảng số…"; ab.disabled = true;
    try {
      await insight(SAMPLE, `${card.title}. ${card.v ? "Giả thuyết: " + card.hyp : card.hyp} (cách xem: ${card.views[vi].label})`, last, t => aiBox.textContent = t);
    } catch (e) { aiBox.textContent = sampleErr(e); } finally { ab.disabled = false; }
  };
  acts.append(ab);
  // chỉ tính khi thẻ sắp vào màn hình
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); draw(); } }, { rootMargin: "600px 0px" });
    io.observe(el);
  } else draw();
}
CARDS.filter(c => c.sec === "data").forEach(c => renderCard(c, $("#cards-data")));
CARDS.filter(c => c.sec === "group").forEach(c => renderCard(c, $("#cards-group")));
STEPS.forEach(s => {
  const sec = h(`<section class="blk st-${s.key}" id="${s.id || "buoc-" + s.key}"><div class="wrap">
    <div class="sec-head"><div class="sec-no">${s.no}</div><div class="eyebrow">${typeof s.no === "number" ? "Bước " + s.no : "Thêm"}</div><h2>${s.title}</h2></div>
    <p class="sec-lead">${s.lead}</p><div class="cards"></div></div></section>`);
  $("#steps").append(sec);
  CARDS.filter(c => c.st === s.key).forEach(c => renderCard(c, $(".cards", sec)));
});

/* ---------- mục lục: đánh dấu mục đang xem */
(function navSpy() {
  const links = [...document.querySelectorAll("#nav a")], map = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { links.forEach(a => a.classList.remove("on")); const a = map.get(e.target.id); if (a) { a.classList.add("on"); a.scrollIntoView({ block: "nearest", inline: "center" }); } } }), { rootMargin: "-45% 0px -50% 0px" });
  map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
})();

/* ============================================================
   Hỏi dữ liệu
   ============================================================ */
function sampleErr(e) {
  const c = e && e.code;
  if (c === "not_granted" || c === "sampling_disabled" || c === "not_declared" || c === "capability_disabled" || c === "capability_removed") return "Trang chưa được phép dùng Claude trong lần xem này. Tải lại trang và chọn Cho phép khi được hỏi.";
  if (c === "rate_limited") return "Đang hỏi quá nhiều cùng lúc hoặc đã hết lượt dùng. Đợi một lúc rồi hỏi lại.";
  if (c === "session_expired") return "Phiên đăng nhập claude.ai đã hết hạn. Đăng nhập lại rồi hỏi tiếp.";
  if (c === "cancelled") return "Đã dừng.";
  if (c === "invalid_json") return "Claude trả lời chưa đúng định dạng. Thử hỏi lại, hoặc hỏi cụ thể hơn (nêu rõ nhóm, năm, thước đo).";
  if (c === "refused") return "Claude không trả lời câu này. Thử diễn đạt khác.";
  return "Không kết nối được tới Claude lúc này. Thử lại sau." + (e && e.message ? " (" + e.message + ")" : "");
}
const SCHEMA = () => `Bạn là trợ lý phân tích số liệu cho một project thống kê mô tả (môn Thống kê, sinh viên Việt Nam). Dữ liệu: VHLSS 2010, 2012, 2014, 28.196 hộ, 63 tỉnh. Mỗi dòng là một hộ. Tiền: nghìn đồng/năm, giá từng năm (không quy đổi lạm phát).

BIẾN dùng được trong biểu thức:
${Object.entries(Eng.VARS).map(([k, v]) => "- " + k + ": " + v).join("\n")}

BIỂU THỨC: số, biến, + - * / ^, so sánh < <= > >= == !=, && || !, chuỗi trong nháy đơn (vd tier=='T4', province=='Hà Nội', area=='Nông thôn'), hàm log (ln), log10, sqrt, abs, min, max, log1p. Biểu thức đúng trả 1, sai trả 0.
CHIỀU CHIA NHÓM (groupBy, tối đa 2): ${Eng.DIM_NOTE}.
PHÉP TÍNH (agg): ${Eng.AGGS}. Mỗi measure có thể có "where" (lọc riêng cho measure đó), "calc" (công thức từ các measure trước: m0, m1… ví dụ "m0/m1"), "hide": true để ẩn measure phụ.

TRẢ VỀ đúng một JSON:
{"title": "tiêu đề ngắn tiếng Việt",
 "query": {"mode": "group" | "box" | "hist" | "points",
           "filter": "biểu thức lọc hộ, bỏ trống nếu không lọc",
           "groupBy": [...], "measures": [{"name": "nhãn tiếng Việt kèm đơn vị", "agg": "...", "expr": "...", "den": "...", "expr2": "...", "p": 0.9, "where": "...", "calc": "...", "hide": false}],
           "sort": {"by": chỉ_số_measure, "desc": true}, "limit": 10, "limitBoth": false,
           "expr": "(chỉ cho box/hist)", "log": false, "bins": 30, "x": "(points)", "y": "(points)"},
 "chart": {"type": "bar" | "stack" | "line" | "hbar" | "pie" | "scatter" | "heat" | "multi" | "table", "fmt": "pct" | "num0" | "num1" | "num2" | "r", "logx": false, "logy": false, "endLabels": false},
 "explain": "1 câu: tính gì, trên hộ nào",
 "cannot": "nếu dữ liệu không trả lời được thì giải thích ngắn, các trường khác để trống"}

QUY TẮC:
- Năm cụ thể thì lọc year==…; so sánh qua các năm dùng groupBy year với tỷ trọng (share), tỷ lệ hộ (pct), median, thứ hạng.
- Thu nhập điển hình dùng median của inc_head (chia 1000 để ra triệu đồng). Tỷ trọng chi = share với den "tot". "Tỷ lệ hộ có X" = pct với expr "X>0".
- "Hộ nghèo" = Q==1, "hộ giàu" = Q==4 trừ khi câu hỏi nói khác. "Không đủ sống" = short (chi thiết yếu > thu nhập).
- Tương quan: corr với log() hai biến tiền và where "X>0" nếu cần; đặt chart "bar" hoặc "heat".
- Theo tỉnh: groupBy ["province"], thường sort desc và limit 10–15, chart "hbar". Nhóm dưới 30 hộ bị loại tự động.
- Chart: 1 chiều + 1 measure -> "bar" (tỉnh thì "hbar"); chiều đầu là year -> "line"; nhiều tỷ trọng cộng lại 100% -> "stack"; 2 measure theo tỉnh -> "scatter"; box khi hỏi phân phối theo nhóm; hist khi hỏi phân phối một biến.

VÍ DỤ:
Hỏi: Tỷ lệ hộ có ô tô theo nhóm tỉnh qua các năm
{"title":"Tỷ lệ hộ có ô tô theo nhóm tỉnh","query":{"mode":"group","groupBy":["year","tier"],"measures":[{"name":"% hộ có ô tô","agg":"pct","expr":"oto>0"}]},"chart":{"type":"line","fmt":"pct1","endLabels":true},"explain":"% hộ có giá trị ô tô > 0, theo năm và nhóm tỉnh."}
Hỏi: Chi giáo dục chiếm bao nhiêu % tổng chi ở thành thị và nông thôn theo Q?
{"title":"Tỷ trọng chi giáo dục theo Q và khu vực","query":{"mode":"group","groupBy":["Q","area"],"measures":[{"name":"Giáo dục / tổng chi (%)","agg":"share","expr":"edu","den":"tot"}]},"chart":{"type":"bar","fmt":"pct1"},"explain":"Tổng chi giáo dục chia tổng chi của nhóm, gộp 3 năm."}
Hỏi: Tỉnh nào có median thu nhập/người cao nhất năm 2014?
{"title":"Top 10 tỉnh theo median thu nhập/người 2014","query":{"mode":"group","filter":"year==2014","groupBy":["province"],"measures":[{"name":"Median thu nhập/người (triệu)","agg":"median","expr":"inc_head/1000"}],"sort":{"by":0,"desc":true},"limit":10},"chart":{"type":"hbar","fmt":"num1"},"explain":"Median thu nhập/người của từng tỉnh năm 2014."}
Hỏi: Hộ Q4 gấp bao nhiêu lần hộ Q1 ở từng nhóm tỉnh?
{"title":"Median Q4 / median Q1 theo nhóm tỉnh","query":{"mode":"group","filter":"year==2014","groupBy":["tier"],"measures":[{"name":"a","agg":"median","expr":"inc_head","where":"Q==4","hide":true},{"name":"b","agg":"median","expr":"inc_head","where":"Q==1","hide":true},{"name":"Q4/Q1 (lần)","calc":"m0/m1"}]},"chart":{"type":"bar","fmt":"num1"},"explain":"Tỷ số median thu nhập/người của Q4 và Q1 trong từng nhóm tỉnh, năm 2014."}
Hỏi: Phân phối tiền điện mỗi người theo Q
{"title":"Tiền điện/người theo Q (2014)","query":{"mode":"box","filter":"year==2014","groupBy":["Q"],"expr":"elec/size","log":true},"chart":{"type":"bar","fmt":"num0"},"explain":"Hộp Q1–Q3 và vạch q(0,1)–q(0,9) của tiền điện/người năm 2014."}`;

async function insight(sample, question, r, onText) {
  const prompt = `Bạn là trợ lý thống kê cho một nhóm sinh viên. Viết nhận xét tiếng Việt về bảng số dưới đây, TRẢ LỜI câu hỏi.
Yêu cầu: 3–5 gạch đầu dòng ngắn (bắt đầu bằng "• "), mỗi dòng có con số cụ thể lấy ĐÚNG từ bảng (định dạng số kiểu Việt Nam: dấu phẩy thập phân). So sánh nhóm cao nhất – thấp nhất, xu hướng theo Q/năm nếu có. Nhóm dưới 30 hộ thì nói không nên kết luận. Không suy diễn nhân quả, không nói về kiểm định giả thuyết. Cuối cùng 1 dòng "Lưu ý:" về cách đọc (ví dụ tiền theo giá từng năm, tương quan không phải nhân quả) và 1 dòng "Kiến thức:" nêu thước đo/chương môn học đã dùng (C1 dữ liệu, C2 thống kê mô tả, C3 tỷ lệ mẫu và n ≥ 30, C4 ước lượng).

Câu hỏi: ${question}

Bảng số (tính trên dữ liệu VHLSS, tiền nghìn đồng trừ khi nhãn ghi triệu):
${Eng.toText(r)}`;
  const res = await sample(prompt, { onText: ({ text }) => onText(text), modelTier: "default" });
  return res.text;
}

(function ask() {
  const input = $("#askInput"), btn = $("#askBtn"), stop = $("#stopBtn"), status = $("#askStatus"), ans = $("#answer"), hist = $("#history");
  $("#sugs").append(...SUGGESTIONS.map(s => { const b = h(`<button type="button" class="sug">${esc(s)}</button>`); b.onclick = () => { input.value = s; input.focus(); }; return b; }));
  let ctl = null;
  status.textContent = "Đang kết nối Claude…";
  const cap = window.claude && window.claude.use ? window.claude.use("sample") : Promise.resolve(null);
  cap.then(s => {
    SAMPLE = s;
    if (!s) { status.textContent = "Hỏi đáp chạy khi mở trang trên claude.ai (dùng Claude của người xem). Ở đây bạn vẫn dùng được mục Tự khám phá và mọi biểu đồ."; btn.disabled = true; return; }
    status.textContent = "Sẵn sàng. Lần hỏi đầu sẽ xin phép dùng Claude trên tài khoản của bạn.";
    document.querySelectorAll(".ask-card").forEach(b => b.hidden = false);
  }).catch(() => { status.textContent = "Không kết nối được Claude."; btn.disabled = true; });
  input.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); btn.click(); } });
  stop.onclick = () => ctl && ctl.abort();
  btn.onclick = async () => {
    const q = input.value.trim(); if (!q || !SAMPLE) return;
    ctl = new AbortController(); btn.disabled = true; stop.hidden = false; ans.hidden = false;
    ans.innerHTML = ""; status.textContent = "Claude đang chuyển câu hỏi thành phép tính…";
    try {
      let spec = await SAMPLE.json(SCHEMA() + "\n\nHỏi: " + q, { signal: ctl.signal, modelTier: "default" });
      let r = null, err = null;
      const tryRun = s => { try { if (s.cannot) return null; r = Eng.run(s.query || {}); if (r.mode === "group" && !r.groups.length) throw new Error("không có nhóm nào sau khi lọc"); err = null; } catch (e) { err = e.message; r = null; } };
      tryRun(spec);
      if (err) {
        status.textContent = "Phép tính chưa chạy được, Claude đang sửa…";
        spec = await SAMPLE.json(SCHEMA() + "\n\nHỏi: " + q + "\n\nJSON trước đó của bạn:\n" + JSON.stringify(spec) + "\n\nLỗi khi chạy: " + err + "\nHãy sửa và trả lại JSON đầy đủ.", { signal: ctl.signal, modelTier: "default" });
        tryRun(spec);
      }
      if (spec.cannot) { status.textContent = ""; ans.innerHTML = `<div class="insight">${esc(spec.cannot)}</div>`; return; }
      if (!r) { status.textContent = ""; ans.innerHTML = `<div class="insight">Chưa tính được câu này (${esc(err || "lỗi")}). Thử hỏi cụ thể hơn: nêu thước đo, nhóm, năm.</div>`; return; }
      const c = spec.chart || {};
      ans.innerHTML = `<h3>${esc(spec.title || q)}</h3><p class="small">${esc(spec.explain || "")}</p><div class="chart" id="ansChart"></div>
        <div class="insight" id="ansText">Claude đang viết nhận xét…</div>
        <details class="how"><summary>Bảng số và cách tính</summary><div class="tbl-wrap" style="margin-top:8px">${Eng.toTable(r)}</div><pre>${esc(JSON.stringify(spec.query, null, 1))}</pre></details>`;
      if (c.type === "table") $("#ansChart").remove(); else Charts.render($("#ansChart"), Eng.toChart(r, c));
      if (r.small && r.small.length) status.textContent = "Có nhóm dưới 30 hộ: " + r.small.slice(0, 6).join(", ") + (r.small.length > 6 ? "…" : "");
      else status.textContent = "";
      await insight(SAMPLE, q, r, t => { const el = $("#ansText"); if (el) el.textContent = t; });
      const chip = h(`<button type="button" class="sug">↺ ${esc(q.length > 48 ? q.slice(0, 46) + "…" : q)}</button>`);
      chip.onclick = () => { input.value = q; btn.click(); }; hist.prepend(chip);
    } catch (e) {
      status.textContent = sampleErr(e);
      const el = $("#ansText"); if (el && e.text) el.textContent = e.text;
    } finally { btn.disabled = false; stop.hidden = true; }
  };
})();

/* ============================================================
   Tự khám phá (không cần Claude)
   ============================================================ */
(function explore() {
  const M = {
    "Median thu nhập/người (triệu)": { agg: "median", expr: "inc_head/1000", fmt: "num1" },
    "Mean thu nhập/người (triệu)": { agg: "mean", expr: "inc_head/1000", fmt: "num1" },
    "CV thu nhập/người (bỏ 1% cao nhất)": { agg: "cv_trim", expr: "inc_head", fmt: "num2" },
    "Tỷ trọng chi thiết yếu (%)": { agg: "share", expr: "nec", den: "tot" },
    "Median chi thiết yếu / thu nhập (%)": { agg: "median", expr: "burden*100", fmt: "num0" },
    "% hộ không đủ tiền cho thiết yếu": { agg: "pct", expr: "short" },
    "% hộ tổng chi > thu nhập": { agg: "pct", expr: "overspend" },
    "Tỷ trọng thực phẩm (%)": { agg: "share", expr: "food", den: "tot" },
    "Tỷ trọng gạo (%)": { agg: "share", expr: "rice", den: "tot" },
    "Tỷ trọng ngoài ăn uống (%)": { agg: "share", expr: "nfood", den: "tot" },
    "Tỷ trọng giáo dục (%)": { agg: "share", expr: "edu", den: "tot" },
    "Tỷ trọng y tế (%)": { agg: "share", expr: "health", den: "tot" },
    "Tỷ trọng thuốc lá (%)": { agg: "share", expr: "tobaco", den: "tot" },
    "Median tiền điện/người (nghìn)": { agg: "median", expr: "elec/size", fmt: "num0" },
    "% hộ trả tiền nước": { agg: "pct", expr: "water>0" },
    "% hộ trả phí rác": { agg: "pct", expr: "garb>0" },
    "% hộ tự đóng BHYT": { agg: "pct", expr: "hins>0" },
    "Median giá nhà (triệu)": { agg: "median", expr: "house/1000", fmt: "num0" },
    "Median nhà / thu nhập (năm)": { agg: "median", expr: "house_to_inc", fmt: "num1" },
    "Median đồ công nghệ (triệu)": { agg: "median", expr: "tech/1000", fmt: "num2" },
    "% hộ có ô tô": { agg: "pct", expr: "oto>0", fmt: "pct1" },
    "% hộ có xe máy": { agg: "pct", expr: "moto>0" },
    "% hộ có điện thoại": { agg: "pct", expr: "tele>0" },
    "Mean số người/hộ": { agg: "mean", expr: "size", fmt: "num2" },
    "Số hộ": { agg: "count", fmt: "num0" },
  };
  const DIM = { "Không chia": null, "Nhóm Q": "Q", "Khu vực": "area", "Nhóm tỉnh": "tier", "Năm": "year", "Tỉnh": "province", "Số người/hộ": "size", "Phạm vi (toàn quốc, khu vực, nhóm tỉnh)": "scope" };
  const opts = (o, sel) => Object.keys(o).map(k => `<option${k === sel ? " selected" : ""}>${k}</option>`).join("");
  const fopts = (arr) => arr.map(([v, t]) => `<option value="${v}">${t}</option>`).join("");
  $("#exPanel").innerHTML = `
    <label>Thước đo<select id="exM">${opts(M, "Tỷ trọng chi thiết yếu (%)")}</select></label>
    <label>Chia theo<select id="exD1">${opts(DIM, "Nhóm Q")}</select></label>
    <label>Chia tiếp theo<select id="exD2">${opts(DIM, "Khu vực")}</select></label>
    <label>Năm<select id="exY">${fopts([["", "Cả 3 năm"], ["2010", "2010"], ["2012", "2012"], ["2014", "2014"]])}</select></label>
    <label>Khu vực<select id="exA">${fopts([["", "Tất cả"], ["Thành thị", "Thành thị"], ["Nông thôn", "Nông thôn"]])}</select></label>
    <label>Nhóm tỉnh<select id="exT">${fopts([["", "Tất cả"], ["T1", "T1"], ["T2", "T2"], ["T3", "T3"], ["T4", "T4"]])}</select></label>
    <label>Nhóm thu nhập<select id="exQ">${fopts([["", "Tất cả"], ["1", "Q1"], ["2", "Q2"], ["3", "Q3"], ["4", "Q4"]])}</select></label>
    <p class="small">Nhóm dưới 30 hộ được tô đỏ trong bảng; theo tỉnh thì bị ẩn.</p>`;
  function draw() {
    const m = M[$("#exM").value], d1 = DIM[$("#exD1").value], d2 = DIM[$("#exD2").value];
    const f = [];
    if ($("#exY").value) f.push("year==" + $("#exY").value);
    if ($("#exA").value) f.push("area=='" + $("#exA").value + "'");
    if ($("#exT").value) f.push("tier=='" + $("#exT").value + "'");
    if ($("#exQ").value) f.push("Q==" + $("#exQ").value);
    const gb = [d1, d2].filter(Boolean).filter((d, i, a) => a.indexOf(d) === i);
    const q = { filter: f.join(" && "), groupBy: gb, measures: [{ name: $("#exM").value, ...m }] };
    if (gb[0] === "province") { q.sort = { by: 0, desc: true }; q.groupBy = ["province"]; }
    try {
      const r = Eng.run(q);
      const type = gb[0] === "province" ? "hbar" : gb[0] === "year" ? "line" : "bar";
      Charts.render($("#exChart"), Eng.toChart(r, { type, fmt: m.fmt, endLabels: type === "line" && gb.length > 1 }));
      $("#exTable").innerHTML = Eng.toTable(r, 70);
    } catch (e) { $("#exChart").innerHTML = `<p class="small">${esc(e.message)}</p>`; }
  }
  document.querySelectorAll("#exPanel select").forEach(s => s.addEventListener("change", draw));
  const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); draw(); } }, { rootMargin: "400px 0px" });
  io.observe($("#kham-pha"));
})();
