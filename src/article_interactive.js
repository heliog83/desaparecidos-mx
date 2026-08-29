(() => {
  "use strict";
  const node = document.getElementById("article-chart-data");
  if (!node) return;
  const DATA = JSON.parse(node.textContent);
  const NS = "http://www.w3.org/2000/svg";
  const COLORS = { alive: "#3c6e91", dead: "#2b2b2b", missing: "#7a1f1f", muted: "#9a9e9a" };
  const fmt = new Intl.NumberFormat("en-US");
  const pct = new Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 1 });

  const svgNode = (tag, attrs = {}, text = "") => {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, String(v)));
    if (text) n.textContent = text;
    return n;
  };
  const clear = (n) => { while (n.firstChild) n.firstChild.remove(); };
  const buttonMode = (root, mode) => {
    root.querySelectorAll("button[data-mode]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.mode === mode)));
  };
  const tooltipFor = (root) => root.querySelector(".chart-tooltip");
  const initThemeToggle = () => {
    const toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;
    const buttons = toggle.querySelectorAll("button[data-theme-set]");
    buttons.forEach((b) => {
      b.addEventListener("click", () => {
        const mode = b.dataset.themeSet;
        if (mode === "auto") {
          delete document.documentElement.dataset.theme;
        } else {
          document.documentElement.dataset.theme = mode;
        }
        buttons.forEach((btn) => btn.setAttribute("aria-pressed", String(btn.dataset.themeSet === mode)));
      });
    });
  };
  initThemeToggle();
  const showTip = (tip, html, x, y) => {
    tip.innerHTML = html;
    tip.style.display = "block";
    tip.style.left = `${Math.max(6, Math.min(x + 14, tip.parentElement.clientWidth - 250))}px`;
    tip.style.top = `${Math.max(4, y - 26)}px`;
  };
  const hideTip = (tip) => { tip.style.display = "none"; };
  const pointerIn = (event, root) => {
    const box = root.getBoundingClientRect();
    return [event.clientX - box.left, event.clientY - box.top];
  };
  const niceMax = (v) => {
    if (v <= 1) return 1;
    const pow = 10 ** Math.floor(Math.log10(v));
    return Math.ceil(v / pow) * pow;
  };
  const pearsonR = (xs, ys) => {
    const n = xs.length;
    if (n < 3) return NaN;
    const mx = xs.reduce((a, b) => a + b, 0) / n;
    const my = ys.reduce((a, b) => a + b, 0) / n;
    let num = 0, dx2 = 0, dy2 = 0;
    for (let i = 0; i < n; i++) {
      const dx = xs[i] - mx, dy = ys[i] - my;
      num += dx * dy; dx2 += dx * dx; dy2 += dy * dy;
    }
    return num / Math.sqrt(dx2 * dy2);
  };
  const median = (arr) => {
    const s = arr.slice().sort((a, b) => a - b);
    const m = Math.floor(s.length / 2);
    return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
  };

  // ---------------------------------------------------------------------------
  // Fig A
  // ---------------------------------------------------------------------------
  function initOutcomes(root) {
    const canvas = root.querySelector(".chart-canvas");
    const summary = root.querySelector(".chart-summary");
    const tip = tooltipFor(root);
    let mode = "absolute";

    function draw() {
      canvas.querySelectorAll("svg").forEach((n) => n.remove());
      hideTip(tip);
      const width = Math.max(300, canvas.clientWidth);
      const height = width < 520 ? 355 : 390;
      const margin = { top: 48, right: 18, bottom: 45, left: width < 520 ? 50 : 66 };
      const innerW = width - margin.left - margin.right;
      const innerH = height - margin.top - margin.bottom;
      const svg = svgNode("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
      svg.append(svgNode("title", {}, "Recorded disappearances by year and current registry outcome"));
      svg.append(svgNode("desc", {}, "Bars for found alive, found dead and still missing."));
      const years = DATA.outcomes;
      const totals = years.map((d) => d.alive + d.dead + d.missing);
      const ymax = mode === "share" ? 1
        : mode === "missing" ? niceMax(Math.max(...years.map((d) => d.missing)))
        : mode === "alive"   ? niceMax(Math.max(...years.map((d) => d.alive)))
        : mode === "dead"    ? niceMax(Math.max(...years.map((d) => d.dead)))
        : niceMax(Math.max(...totals));
      const y = (v) => margin.top + innerH - (v / ymax) * innerH;
      const step = innerW / years.length;
      const bw = Math.max(4, step * 0.78);

      for (let i = 0; i <= 4; i++) {
        const v = ymax * i / 4, yy = y(v);
        svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-grid" }));
        const tick = mode === "share" ? `${Math.round(v * 100)}%`
          : (v >= 1000 ? `${Math.round(v / 1000)}k` : String(Math.round(v)));
        svg.append(svgNode("text", { x: margin.left - 8, y: yy + 4, "text-anchor": "end", class: "chart-label" }, tick));
      }
      svg.append(svgNode("line", { x1: margin.left, x2: margin.left, y1: margin.top, y2: margin.top + innerH, class: "chart-axis" }));
      svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: margin.top + innerH, y2: margin.top + innerH, class: "chart-axis" }));

      const SEXENIOS = [
        [2006, "Calder\u00F3n"], [2012, "Pe\u00F1a Nieto"],
        [2018, "L\u00F3pez Obrador"], [2024, "Sheinbaum"],
      ];
      const firstYear = years[0].year;
      SEXENIOS.forEach(([startYear, name]) => {
        const idx = startYear - firstYear;
        if (idx < 0 || idx >= years.length) return;
        const gx = margin.left + idx * step;
        svg.append(svgNode("line", { x1: gx, x2: gx, y1: margin.top, y2: margin.top + innerH, class: "chart-sexenio" }));
        if (width >= 560) {
          svg.append(svgNode("text", { x: gx + 3, y: margin.top - 8, "text-anchor": "start", class: "chart-sexenio-label" }, name));
        }
      });

      const isSingle = ["missing", "alive", "dead"].includes(mode);
      years.forEach((d, i) => {
        const total = totals[i];
        const vals = isSingle ? [d[mode]] : (mode === "share" ? [d.alive, d.dead, d.missing] : [d.alive, d.dead, d.missing]);
        const keys = isSingle ? [mode] : ["alive", "dead", "missing"];
        let cumulative = 0;
        vals.forEach((raw, j) => {
          const val = mode === "share" ? raw / total : raw;
          const x = margin.left + i * step + (step - bw) / 2;
          const top = y(cumulative + val);
          const bottom = y(cumulative);
          const rect = svgNode("rect", { x, y: top, width: bw, height: Math.max(0, bottom - top), fill: COLORS[keys[j]], tabindex: 0 });
          rect.setAttribute("aria-label", `${d.year}: ${keys[j]}, ${fmt.format(raw)} people`);
          const tooltipHtml = `<strong>${d.year}</strong><br>Still missing <strong>${fmt.format(d.missing)}</strong> (${pct.format(d.missing / total)})<br>Found alive ${fmt.format(d.alive)} (${pct.format(d.alive / total)})<br>Found dead ${fmt.format(d.dead)} (${pct.format(d.dead / total)})<br>Total reported ${fmt.format(total)}`;
          rect.addEventListener("mouseenter", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tooltipHtml, px, py); });
          rect.addEventListener("mousemove", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tip.innerHTML, px, py); });
          rect.addEventListener("mouseleave", () => hideTip(tip));
          rect.addEventListener("focus", () => showTip(tip, tooltipHtml, x, top));
          rect.addEventListener("blur", () => hideTip(tip));
          svg.append(rect);
          cumulative += val;
        });
        if (d.year % 5 === 0 || d.year === 2025) {
          svg.append(svgNode("text", { x: margin.left + (i + 0.5) * step, y: height - 18, "text-anchor": "middle", class: "chart-label" }, String(d.year)));
        }
      });

      const legendItems = mode === "missing" ? [["Still missing \u2014 each bar starts at zero", COLORS.missing]]
        : mode === "alive"   ? [["Found alive \u2014 each bar starts at zero", COLORS.alive]]
        : mode === "dead"    ? [["Found dead \u2014 each bar starts at zero", COLORS.dead]]
        : [["Found alive", COLORS.alive], ["Found dead", COLORS.dead], ["Still missing", COLORS.missing]];
      const legendStep = innerW / legendItems.length;
      legendItems.forEach(([label, color], index) => {
        const lx = margin.left + index * legendStep;
        svg.append(svgNode("rect", { x: lx, y: 5, width: 10, height: 10, fill: color }));
        svg.append(svgNode("text", { x: lx + 15, y: 14, class: "chart-label" }, label));
      });
      canvas.append(svg);
      summary.innerHTML = mode === "share"
        ? "Shares describe each cohort\u2019s <strong>current registry status</strong>; they do not show when a person was located."
        : mode === "missing" ? "Every red bar starts at <strong>zero</strong>, so annual still-missing counts can be compared directly. These are current outcomes, not the number newly missing that year."
        : mode === "alive"   ? "Every blue bar starts at <strong>zero</strong>, so annual found-alive counts can be compared directly. These are current registry statuses."
        : mode === "dead"    ? "Every dark bar starts at <strong>zero</strong>, so annual found-dead counts can be compared directly. These are current registry statuses."
        : "Each stacked bar is a recorded year-of-disappearance cohort, not a cumulative total.";
    }
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      mode = b.dataset.mode; buttonMode(root, mode); draw();
    }));
    new ResizeObserver(draw).observe(canvas);
    draw();
  }

  // ---------------------------------------------------------------------------
  // Fig B map
  // ---------------------------------------------------------------------------
  function initMap(root) {
    const canvas = root.querySelector(".map-canvas");
    const legend = root.querySelector(".map-legend");
    const detail = root.querySelector(".map-detail");
    const tip = tooltipFor(root);
    const stateByCode = new Map(DATA.states.map((d) => [d.cve, d]));
    const PALETTES = {
      rate:         ["#fde8d8", "#f0b49a", "#d46f55", "#a33030", "#6b0f0f"],
      count:        ["#fde8d8", "#f0b49a", "#d46f55", "#a33030", "#6b0f0f"],
      confidential: ["#e8edf2", "#b8c9d8", "#7a9db5", "#3c6e91", "#1a3a52"],
    };
    const specs = {
      rate:         { key: "rate",               thresholds: [50, 100, 175, 260],       labels: ["0\u201350", "50\u2013100", "100\u2013175", "175\u2013260", "260+"],  title: "unresolved records per 100,000" },
      count:        { key: "count",              thresholds: [500, 2000, 5000, 10000],   labels: ["0\u2013500", "500\u20132k", "2k\u20135k", "5k\u201310k", "10k+"],   title: "unresolved records" },
      confidential: { key: "confidential_share", thresholds: [0.15, 0.30, 0.45, 0.60],  labels: ["0\u201315%", "15\u201330%", "30\u201345%", "45\u201360%", "60%+"],  title: "share confidential" },
    };
    let metric = "rate";
    let selected = "28";

    const colorFor = (value, thresholds, palette) => {
      const index = thresholds.findIndex((limit) => value < limit);
      return palette[index === -1 ? palette.length - 1 : index];
    };
    const stateHtml = (d) => `<strong>${d.label}</strong><br>`
      + `Unresolved <strong>${fmt.format(d.count)}</strong><br>`
      + `Rate ${d.rate.toFixed(1)} per 100,000<br>`
      + `Confidential ${fmt.format(d.confidential_count)} (${pct.format(d.confidential_share)})<br>`
      + `<span class="tooltip-vintage">Snapshot: 2 Dec 2025</span>`;
    const stateAria = (d) => `${d.label}: ${fmt.format(d.count)} unresolved records, ${d.rate.toFixed(1)} per 100,000, ${pct.format(d.confidential_share)} confidential`;

    function draw() {
      canvas.querySelectorAll("svg").forEach((n) => n.remove());
      hideTip(tip);
      const spec = specs[metric];
      const palette = PALETTES[metric];
      const svg = svgNode("svg", { viewBox: "0 0 900 520", role: "img", "aria-label": `Map of Mexico coloured by ${spec.title}` });
      svg.append(svgNode("title", {}, `Mexico: ${spec.title}`));
      svg.append(svgNode("desc", {}, "Each state can be focused or pointed to for unresolved count, rate and confidential share."));
      DATA.map_paths.forEach((feature) => {
        const d = stateByCode.get(feature.cve);
        if (!d) return;
        const path = svgNode("path", {
          d: feature.d,
          fill: colorFor(d[spec.key], spec.thresholds, palette),
          stroke: "#fff", "stroke-width": "0.8",
          class: `map-state${selected === feature.cve ? " is-selected" : ""}`,
          tabindex: 0, "fill-rule": "evenodd",
        });
        path.setAttribute("aria-label", stateAria(d));
        path.addEventListener("mouseenter", (event) => { const [x, y] = pointerIn(event, canvas); showTip(tip, stateHtml(d), x, y); });
        path.addEventListener("mousemove", (event) => { const [x, y] = pointerIn(event, canvas); showTip(tip, stateHtml(d), x, y); });
        path.addEventListener("mouseleave", () => hideTip(tip));
        path.addEventListener("focus", () => showTip(tip, stateHtml(d), 12, 12));
        path.addEventListener("blur", () => hideTip(tip));
        path.addEventListener("click", () => {
          selected = feature.cve;
          draw();
          document.dispatchEvent(new CustomEvent("state-select", { detail: { name: d.name } }));
        });
        svg.append(path);
      });
      canvas.append(svg);
      legend.innerHTML = spec.labels.map((label, i) =>
        `<span><i style="background:${palette[i]}"></i>${label}</span>`).join("");
      const d = stateByCode.get(selected);
      detail.innerHTML = d ? `<strong>${d.label}</strong><span><b>${fmt.format(d.count)}</b> unresolved</span><span><b>${d.rate.toFixed(1)}</b> per 100,000</span><span><b>${fmt.format(d.confidential_count)}</b> confidential (${pct.format(d.confidential_share)})</span><span>Snapshot: 2 Dec 2025</span>` : "";
    }
    root.querySelectorAll("button[data-mode]").forEach((button) => button.addEventListener("click", () => {
      metric = button.dataset.mode; buttonMode(root, metric); draw();
    }));
    document.addEventListener("state-select", (e) => {
      const match = DATA.states.find((d) => d.name === e.detail.name);
      if (match && match.cve) { selected = match.cve; draw(); }
    });
    draw();
  }

  // ---------------------------------------------------------------------------
  // State bar chart (linked + median)
  // ---------------------------------------------------------------------------
  function initStates(root) {
    const bars = root.querySelector(".state-bars");
    const detail = root.querySelector(".state-detail");
    const select = root.querySelector("select");
    let metric = "rate";
    let selected = "TAMAULIPAS";
    const metrics = {
      rate:         { key: "rate",               label: "per 100,000", format: (v) => v.toFixed(1) },
      count:        { key: "count",              label: "records",     format: (v) => fmt.format(v) },
      confidential: { key: "confidential_share", label: "confidential", format: (v) => pct.format(v) },
    };
    DATA.states.slice().sort((a, b) => a.name.localeCompare(b.name, "es")).forEach((d) => {
      const o = document.createElement("option"); o.value = d.name; o.textContent = d.label; select.append(o);
    });
    select.value = selected;

    function render() {
      clear(bars);
      const spec = metrics[metric];
      const ranked = DATA.states.slice().sort((a, b) => b[spec.key] - a[spec.key]);
      let shown = ranked;
      const max = Math.max(...ranked.map((d) => d[spec.key]));
      const med = median(DATA.states.map((d) => d[spec.key]));

      shown.forEach((d) => {
        const row = document.createElement("button");
        row.type = "button"; row.className = "state-row";
        row.setAttribute("aria-current", String(d.name === selected));
        row.setAttribute("aria-label", `${d.label}: ${spec.format(d[spec.key])} ${spec.label}`);
        const barPct = Math.max(0.5, d[spec.key] / max * 100);
        const medPct = med / max * 100;
        row.innerHTML = `<span class="state-name">${d.label}</span>`
          + `<span class="state-bar-track">`
          + `<span class="state-bar" style="width:${barPct}%"></span>`
          + `<span class="state-median-tick" style="left:${medPct}%" aria-hidden="true"></span>`
          + `</span>`
          + `<span class="state-number">${spec.format(d[spec.key])}</span>`;
        row.addEventListener("click", () => {
          selected = d.name; select.value = selected; render();
          document.dispatchEvent(new CustomEvent("state-select", { detail: { name: d.name } }));
        });
        bars.append(row);
      });

      // Median caption row
      const medRow = document.createElement("p");
      medRow.className = "state-median-caption";
      medRow.innerHTML = `<span style="display:inline-block;width:1px;height:10px;background:#585D59;vertical-align:middle;margin-right:5px"></span>Median: <strong>${spec.format(med)}</strong>`;
      bars.append(medRow);

      const selectedRow = DATA.states.find((d) => d.name === selected);
      if (selectedRow) detail.innerHTML = `<strong>${selectedRow.label}</strong><span><b>${fmt.format(selectedRow.count)}</b> unresolved records</span><span><b>${selectedRow.rate.toFixed(1)}</b> per 100,000</span><span><b>${pct.format(selectedRow.confidential_share)}</b> confidential</span><span>Snapshot: 2 Dec 2025</span>`;
    }
    select.addEventListener("change", () => { selected = select.value; render(); });
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      metric = b.dataset.mode; buttonMode(root, metric); render();
    }));
    document.addEventListener("state-select", (e) => {
      selected = e.detail.name; select.value = selected; render();
    });
    render();
  }

  // ---------------------------------------------------------------------------
  // Fig C - Interactive confidential share ranking
  // ---------------------------------------------------------------------------
  function initConfidential(root) {
    const canvas = root.querySelector(".chart-canvas");
    const summary = root.querySelector(".chart-summary");
    const tip = tooltipFor(root);
    let sortKey = "confidential_share";
    const HIGHLIGHT = { "JALISCO": true, "GUERRERO": true, "NAYARIT": true, "COLIMA": true, "YUCATAN": true };
    // Formatter depends on which metric is being sorted
    const fmtVal = (key, v) => key === "confidential_share" ? pct.format(v) : v.toFixed(1);

    function draw() {
      canvas.querySelectorAll("svg").forEach((n) => n.remove());
      hideTip(tip);
      const sorted = DATA.states.slice().sort((a, b) => b[sortKey] - a[sortKey]);
      const width = Math.max(300, canvas.clientWidth);
      const rowH = 20, gap = 4;
      const margin = { top: 28, right: 64, bottom: 32, left: width < 520 ? 118 : 165 };
      const innerW = width - margin.left - margin.right;
      const innerH = sorted.length * (rowH + gap);
      const height = innerH + margin.top + margin.bottom;
      const maxVal = Math.max(...sorted.map((d) => d[sortKey]));
      const medVal = median(sorted.map((d) => d[sortKey]));
      const xv = (v) => margin.left + (v / maxVal) * innerW;
      const natAvg = DATA.states.reduce((s, d) => s + d.confidential_share, 0) / DATA.states.length;
      const svg = svgNode("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
      svg.append(svgNode("title", {}, "Confidential share of unresolved records by state"));

      // Median reference line
      const medX = xv(medVal);
      svg.append(svgNode("line", { x1: medX, x2: medX, y1: margin.top - 18, y2: margin.top + innerH, stroke: "#585D59", "stroke-width": 1, "stroke-dasharray": "3 3" }));
      svg.append(svgNode("text", { x: medX + 3, y: margin.top - 6, class: "chart-muted" }, `Median ${fmtVal(sortKey, medVal)}`));

      sorted.forEach((d, i) => {
        const yy = margin.top + i * (rowH + gap);
        const isHi = !!HIGHLIGHT[d.name];
        const barColor = isHi ? "#7a1f1f" : "#b9b4aa";
        const barW = Math.max(2, (d[sortKey] / maxVal) * innerW);
        svg.append(svgNode("text", {
          x: margin.left - 7, y: yy + rowH * 0.7,
          "text-anchor": "end", class: isHi ? "chart-value" : "chart-label",
        }, d.label));
        const rect = svgNode("rect", { x: margin.left, y: yy + 2, width: barW, height: rowH - 4, fill: barColor, tabindex: 0 });
        rect.setAttribute("aria-label", `${d.label}: ${fmtVal(sortKey, d[sortKey])}`);
        const tipHtml = `<strong>${d.label}</strong><br>Confidential <strong>${pct.format(d.confidential_share)}</strong> (${fmt.format(d.confidential_count)} of ${fmt.format(d.count)})<br>Rate ${d.rate.toFixed(1)} per 100,000<br><span class="tooltip-vintage">Snapshot: 2 Dec 2025</span>`;
        rect.addEventListener("mouseenter", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tipHtml, px, py); });
        rect.addEventListener("mousemove", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tipHtml, px, py); });
        rect.addEventListener("mouseleave", () => hideTip(tip));
        rect.addEventListener("focus", () => showTip(tip, tipHtml, margin.left + barW + 4, yy));
        rect.addEventListener("blur", () => hideTip(tip));
        svg.append(rect);
        svg.append(svgNode("text", { x: margin.left + barW + 5, y: yy + rowH * 0.7, class: "chart-label" }, fmtVal(sortKey, d[sortKey])));
      });
      // X axis ticks
      for (let t = 0; t <= 4; t++) {
        const v = t / 4 * maxVal, tx = xv(v);
        svg.append(svgNode("line", { x1: tx, x2: tx, y1: margin.top + innerH, y2: margin.top + innerH + 4, stroke: "#8d918d", "stroke-width": 1 }));
        svg.append(svgNode("text", { x: tx, y: margin.top + innerH + 14, "text-anchor": "middle", class: "chart-label" }, fmtVal(sortKey, v)));
      }
      canvas.append(svg);
      summary.innerHTML = `National average: <strong>${pct.format(natAvg)}</strong>. Jalisco (${pct.format(DATA.states.find((d) => d.name === "JALISCO").confidential_share)}) and Nayarit redact the most; Guerrero and Colima the least.`;
    }
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      sortKey = b.dataset.mode; buttonMode(root, sortKey); draw();
    }));
    new ResizeObserver(draw).observe(canvas);
    draw();
  }

  // ---------------------------------------------------------------------------
  // Fig D - Scatter with variable selector
  // ---------------------------------------------------------------------------
  function initScatter(root) {
    const canvas = root.querySelector(".chart-canvas");
    const summary = root.querySelector(".chart-summary");
    const tip = tooltipFor(root);
    const varSelect = root.querySelector("#scatter-var");
    const HIGHLIGHT = { "JALISCO": "#7a1f1f", "GUERRERO": "#3c6e91", "COLIMA": "#5a8a3a", "YUCATAN": "#7a5aaa" };
    const VAR_META = {
      homicide_rate:      { label: "Homicide rate per 100k (2015\u20132025)",     fmt: (v) => v.toFixed(1) },
      pibe_per_capita:    { label: "GDP per capita (MXN 2018)",                    fmt: (v) => `$${fmt.format(Math.round(v/1000))}k` },
      corruption_per100k: { label: "Corruption prevalence per 100k (2025)",       fmt: (v) => fmt.format(Math.round(v)) },
      kidnapping_per100k: { label: "Kidnapping rate per 100k (2015\u20132025)",   fmt: (v) => v.toFixed(3) },
      femicide_per100k:   { label: "Femicide rate per 100k (2015\u20132025)",     fmt: (v) => v.toFixed(3) },
      resolution_share:   { label: "Resolution share (% of records located)",     fmt: (v) => pct.format(v) },
    };

    function draw() {
      canvas.querySelectorAll("svg").forEach((n) => n.remove());
      hideTip(tip);
      const xKey = varSelect ? varSelect.value : "homicide_rate";
      const xMeta = VAR_META[xKey] || VAR_META.homicide_rate;
      const states = DATA.states.filter((d) => d[xKey] !== undefined && d[xKey] > 0);
      const xs = states.map((d) => d[xKey]);
      const ys = states.map((d) => d.confidential_share);
      const r = pearsonR(xs, ys);
      const width = Math.max(300, canvas.clientWidth);
      const height = width < 520 ? 320 : 360;
      const margin = { top: 24, right: 24, bottom: 56, left: 58 };
      const innerW = width - margin.left - margin.right;
      const innerH = height - margin.top - margin.bottom;
      const xmax = Math.max(...xs) * 1.1;
      const sx = (v) => margin.left + (v / xmax) * innerW;
      const sy = (v) => margin.top + innerH - v * innerH;
      const svg = svgNode("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
      svg.append(svgNode("title", {}, `Confidential share vs ${xMeta.label}`));
      // Grid
      for (let i = 0; i <= 4; i++) {
        const yv = i / 4, yy = sy(yv);
        svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-grid" }));
        svg.append(svgNode("text", { x: margin.left - 6, y: yy + 4, "text-anchor": "end", class: "chart-label" }, `${Math.round(yv * 100)}%`));
        const xv = i / 4 * xmax, xx = sx(xv);
        svg.append(svgNode("line", { x1: xx, x2: xx, y1: margin.top, y2: margin.top + innerH, class: "chart-grid" }));
        svg.append(svgNode("text", { x: xx, y: height - 8, "text-anchor": "middle", class: "chart-label" }, xMeta.fmt(xv)));
      }
      svg.append(svgNode("line", { x1: margin.left, x2: margin.left, y1: margin.top, y2: margin.top + innerH, class: "chart-axis" }));
      svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: margin.top + innerH, y2: margin.top + innerH, class: "chart-axis" }));
      // Regression line
      const n = xs.length;
      const mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
      let num = 0, den = 0;
      for (let i = 0; i < n; i++) { num += (xs[i] - mx) * (ys[i] - my); den += (xs[i] - mx) ** 2; }
      if (den > 0) {
        const slope = num / den, intercept = my - slope * mx;
        const ry0 = Math.min(1, Math.max(0, intercept));
        const ry1 = Math.min(1, Math.max(0, intercept + slope * xmax));
        svg.append(svgNode("line", { x1: sx(0), x2: sx(xmax), y1: sy(ry0), y2: sy(ry1), stroke: "#8d918d", "stroke-width": 1.5, "stroke-dasharray": "4 3" }));
      }
      // Dots
      states.forEach((d) => {
        const cx = sx(d[xKey]), cy = sy(d.confidential_share);
        const hiColor = HIGHLIGHT[d.name];
        const fill = hiColor || "#9a9e9a";
        const rdot = hiColor ? 11 : 7.5;
        const circle = svgNode("circle", { cx, cy, r: rdot, fill, opacity: hiColor ? 1 : 0.7, tabindex: 0 });
        const tipHtml = `<strong>${d.label}</strong><br>Confidential <strong>${pct.format(d.confidential_share)}</strong><br>${xMeta.label}: <strong>${xMeta.fmt(d[xKey])}</strong><br>Unresolved ${fmt.format(d.count)} \u00B7 Rate ${d.rate.toFixed(1)}`;
        circle.setAttribute("aria-label", `${d.label}: confidential ${pct.format(d.confidential_share)}`);
        if (hiColor && width >= 420) {
          svg.append(svgNode("text", { x: cx + 14, y: cy + 4, class: "chart-label", fill: hiColor }, d.label));
        }
        circle.addEventListener("mouseenter", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tipHtml, px, py); });
        circle.addEventListener("mousemove", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, tipHtml, px, py); });
        circle.addEventListener("mouseleave", () => hideTip(tip));
        circle.addEventListener("focus", () => showTip(tip, tipHtml, cx, cy));
        circle.addEventListener("blur", () => hideTip(tip));
        svg.append(circle);
      });
      svg.append(svgNode("text", { x: 11, y: margin.top + innerH / 2, "text-anchor": "middle", transform: `rotate(-90,11,${margin.top + innerH / 2})`, class: "chart-muted" }, "Confidential share"));
      canvas.append(svg);
      const dir = r < 0 ? "negative" : "positive";
      summary.innerHTML = `Pearson <em>r</em> = <strong>${r.toFixed(2)}</strong> (${dir} association, ${states.length} states). Ecological comparison \u2014 describes states, not individual cases.`;
    }
    if (varSelect) varSelect.addEventListener("change", draw);
    new ResizeObserver(draw).observe(canvas);
    draw();
  }

  // ---------------------------------------------------------------------------
  // Fig H - Snapshots
  // ---------------------------------------------------------------------------
  function initSnapshots(root) {
    const canvas = root.querySelector(".chart-canvas");
    const summary = root.querySelector(".chart-summary");
    const tip = tooltipFor(root);
    const select = root.querySelector("select");
    let metric = "share";
    let selected = "NATIONAL";
    const states = [...new Set(DATA.snapshots.map((d) => d.name))]
      .filter((name) => name !== "Se Desconoce")
      .sort((a, b) => a.localeCompare(b, "es"));
    ["NATIONAL", ...states].forEach((name) => {
      const o = document.createElement("option"); o.value = name; o.textContent = name === "NATIONAL" ? "Mexico - national" : name; select.append(o);
    });

    function series() {
      if (selected !== "NATIONAL") return DATA.snapshots.filter((d) => d.name === selected).sort((a, b) => a.snapshot.localeCompare(b.snapshot));
      const byDate = new Map();
      DATA.snapshots.forEach((d) => {
        const cur = byDate.get(d.snapshot) || { snapshot: d.snapshot, name: "NATIONAL", total: 0, conf: 0 };
        cur.total += d.total; cur.conf += d.conf; byDate.set(d.snapshot, cur);
      });
      return [...byDate.values()].sort((a, b) => a.snapshot.localeCompare(b.snapshot));
    }
    function draw() {
      canvas.querySelectorAll("svg").forEach((n) => n.remove());
      hideTip(tip);
      const values = series().map((d) => ({ ...d, share: d.conf / d.total }));
      const width = Math.max(300, canvas.clientWidth), height = width < 520 ? 330 : 360;
      const margin = { top: 20, right: 22, bottom: 48, left: width < 520 ? 54 : 72 };
      const innerW = width - margin.left - margin.right, innerH = height - margin.top - margin.bottom;
      const raw = values.map((d) => d[metric]);
      const minRaw = Math.min(...raw), maxRaw = Math.max(...raw), span = Math.max(maxRaw - minRaw, maxRaw * 0.05 || 1);
      const ymin = metric === "share" ? Math.max(0, minRaw - span * 0.25) : Math.max(0, minRaw - span * 0.35);
      const ymax = maxRaw + span * 0.25;
      const x = (i) => margin.left + (values.length === 1 ? innerW / 2 : i / (values.length - 1) * innerW);
      const y = (v) => margin.top + innerH - (v - ymin) / (ymax - ymin) * innerH;
      const svg = svgNode("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
      svg.append(svgNode("title", {}, `Registry snapshots for ${selected}`));
      for (let i = 0; i <= 4; i++) {
        const v = ymin + (ymax - ymin) * i / 4, yy = y(v);
        svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-grid" }));
        const tick = metric === "share" ? pct.format(v) : (v >= 1000 ? `${(v / 1000).toFixed(v >= 10000 ? 0 : 1)}k` : fmt.format(Math.round(v)));
        svg.append(svgNode("text", { x: margin.left - 8, y: yy + 4, "text-anchor": "end", class: "chart-label" }, tick));
      }
      svg.append(svgNode("line", { x1: margin.left, x2: margin.left, y1: margin.top, y2: margin.top + innerH, class: "chart-axis" }));
      svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: margin.top + innerH, y2: margin.top + innerH, class: "chart-axis" }));
      const points = values.map((d, i) => `${x(i)},${y(d[metric])}`).join(" ");
      svg.append(svgNode("polyline", { points, fill: "none", stroke: "#7a1f1f", "stroke-width": 2.5 }));
      values.forEach((d, i) => {
        const label = new Date(`${d.snapshot}T12:00:00`).toLocaleDateString("en-US", { month: "short" });
        svg.append(svgNode("text", { x: x(i), y: height - 18, "text-anchor": "middle", class: "chart-label" }, label));
        const c = svgNode("circle", { cx: x(i), cy: y(d[metric]), r: 5, fill: "#7a1f1f", tabindex: 0 });
        const h = `<strong>${d.snapshot}</strong><br>Total ${fmt.format(d.total)}<br>Confidential ${fmt.format(d.conf)}<br>Share ${pct.format(d.share)}`;
        c.setAttribute("aria-label", `${d.snapshot}: ${fmt.format(d.conf)} confidential of ${fmt.format(d.total)}`);
        c.addEventListener("mouseenter", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, h, px, py); });
        c.addEventListener("mousemove", (e) => { const [px, py] = pointerIn(e, canvas); showTip(tip, h, px, py); });
        c.addEventListener("mouseleave", () => hideTip(tip));
        c.addEventListener("focus", () => showTip(tip, h, x(i), y(d[metric])));
        c.addEventListener("blur", () => hideTip(tip));
        svg.append(c);
      });
      canvas.append(svg);
      const first = values[0], last = values[values.length - 1];
      summary.innerHTML = `<strong>${selected === "NATIONAL" ? "Mexico" : selected}</strong>: ${fmt.format(first.conf)} to ${fmt.format(last.conf)} confidential records; ${pct.format(first.share)} to ${pct.format(last.share)} of unresolved records.`;
    }
    select.addEventListener("change", () => { selected = select.value; draw(); });
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      metric = b.dataset.mode; buttonMode(root, metric); draw();
    }));
    new ResizeObserver(draw).observe(canvas);
    draw();
  }

  document.querySelectorAll('[data-chart="outcomes"]').forEach(initOutcomes);
  document.querySelectorAll('[data-chart="map"]').forEach(initMap);
  document.querySelectorAll('[data-chart="states"]').forEach(initStates);
  document.querySelectorAll('[data-chart="confidential"]').forEach(initConfidential);
  document.querySelectorAll('[data-chart="scatter"]').forEach(initScatter);
  document.querySelectorAll('[data-chart="snapshots"]').forEach(initSnapshots);
})();
