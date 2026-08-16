(() => {
  "use strict";
  const node = document.getElementById("article-chart-data");
  if (!node) return;
  const DATA = JSON.parse(node.textContent);
  const NS = "http://www.w3.org/2000/svg";
  const COLORS = { alive: "#8fadc4", dead: "#2b2b2b", missing: "#7a1f1f", muted: "#9a9e9a" };
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
  const showTip = (tip, html, x, y) => {
    tip.innerHTML = html;
    tip.style.display = "block";
    tip.style.left = `${Math.max(6, Math.min(x + 12, tip.parentElement.clientWidth - 245))}px`;
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

  function initOutcomes(root) {
    const canvas = root.querySelector(".chart-canvas");
    const summary = root.querySelector(".chart-summary");
    const tip = tooltipFor(root);
    let mode = "absolute";

    function draw() {
      clear(canvas);
      const width = Math.max(300, canvas.clientWidth);
      const height = width < 520 ? 355 : 390;
      const margin = { top: 28, right: 18, bottom: 45, left: width < 520 ? 50 : 66 };
      const innerW = width - margin.left - margin.right;
      const innerH = height - margin.top - margin.bottom;
      const svg = svgNode("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
      svg.append(svgNode("title", {}, "Recorded disappearances by year and current registry outcome"));
      svg.append(svgNode("desc", {}, "Stacked bars for found alive, found dead and still missing. Controls switch between counts and shares."));
      const years = DATA.outcomes;
      const totals = years.map((d) => d.alive + d.dead + d.missing);
      const ymax = mode === "share" ? 1 : niceMax(Math.max(...totals));
      const y = (v) => margin.top + innerH - (v / ymax) * innerH;
      const step = innerW / years.length;
      const bw = Math.max(4, step * 0.78);

      for (let i = 0; i <= 4; i++) {
        const v = ymax * i / 4;
        const yy = y(v);
        svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-grid" }));
        const tick = mode === "share"
          ? `${Math.round(v * 100)}%`
          : (v >= 1000 ? `${Math.round(v / 1000)}k` : String(Math.round(v)));
        svg.append(svgNode("text", { x: margin.left - 8, y: yy + 4, "text-anchor": "end", class: "chart-label" }, tick));
      }
      svg.append(svgNode("line", { x1: margin.left, x2: margin.left, y1: margin.top, y2: margin.top + innerH, class: "chart-axis" }));
      svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: margin.top + innerH, y2: margin.top + innerH, class: "chart-axis" }));

      years.forEach((d, i) => {
        const total = totals[i];
        const vals = [d.alive, d.dead, d.missing];
        const keys = ["alive", "dead", "missing"];
        let cumulative = 0;
        vals.forEach((raw, j) => {
          const val = mode === "share" ? raw / total : raw;
          const x = margin.left + i * step + (step - bw) / 2;
          const top = y(cumulative + val);
          const bottom = y(cumulative);
          const rect = svgNode("rect", { x, y: top, width: bw, height: Math.max(0, bottom - top), fill: COLORS[keys[j]], tabindex: 0 });
          rect.setAttribute("aria-label", `${d.year}: ${keys[j]}, ${fmt.format(raw)} people`);
          rect.addEventListener("mouseenter", (e) => {
            const [px, py] = pointerIn(e, canvas);
            showTip(tip, `<strong>${d.year}</strong><br>Found alive ${fmt.format(d.alive)}<br>Found dead ${fmt.format(d.dead)}<br>Still missing ${fmt.format(d.missing)}<br>Total ${fmt.format(total)}`, px, py);
          });
          rect.addEventListener("mousemove", (e) => {
            const [px, py] = pointerIn(e, canvas);
            showTip(tip, tip.innerHTML, px, py);
          });
          rect.addEventListener("mouseleave", () => hideTip(tip));
          rect.addEventListener("focus", () => showTip(tip,
            `<strong>${d.year}</strong><br>Found alive ${fmt.format(d.alive)}<br>Found dead ${fmt.format(d.dead)}<br>Still missing ${fmt.format(d.missing)}<br>Total ${fmt.format(total)}`,
            x, top));
          rect.addEventListener("blur", () => hideTip(tip));
          svg.append(rect);
          cumulative += val;
        });
        if (d.year % 5 === 0 || d.year === 2025) {
          svg.append(svgNode("text", { x: margin.left + (i + 0.5) * step, y: height - 18, "text-anchor": "middle", class: "chart-label" }, String(d.year)));
        }
      });
      const legend = [["Found alive", COLORS.alive], ["Found dead", COLORS.dead], ["Still missing", COLORS.missing]];
      const legendStep = innerW / legend.length;
      legend.forEach(([label, color], index) => {
        const lx = margin.left + index * legendStep;
        svg.append(svgNode("rect", { x: lx, y: 5, width: 10, height: 10, fill: color }));
        svg.append(svgNode("text", { x: lx + 15, y: 14, class: "chart-label" }, label));
      });
      canvas.append(svg);
      summary.innerHTML = mode === "share"
        ? "Shares describe each cohort's <strong>current registry status</strong>; they do not show when a person was located."
        : "Each bar is a recorded year-of-disappearance cohort, not a cumulative total.";
    }
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      mode = b.dataset.mode;
      buttonMode(root, mode);
      draw();
    }));
    new ResizeObserver(draw).observe(canvas);
    draw();
  }

  function initStates(root) {
    const bars = root.querySelector(".state-bars");
    const detail = root.querySelector(".state-detail");
    const select = root.querySelector("select");
    let metric = "rate";
    let selected = "TAMAULIPAS";
    const metrics = {
      rate: { key: "rate", label: "per 100,000", format: (v) => v.toFixed(1) },
      count: { key: "count", label: "records", format: (v) => fmt.format(v) },
      confidential: { key: "confidential_share", label: "confidential", format: (v) => pct.format(v) }
    };
    DATA.states.slice().sort((a, b) => a.name.localeCompare(b.name, "es")).forEach((d) => {
      const o = document.createElement("option"); o.value = d.name; o.textContent = d.label; select.append(o);
    });
    select.value = selected;

    function render() {
      clear(bars);
      const spec = metrics[metric];
      const ranked = DATA.states.slice().sort((a, b) => b[spec.key] - a[spec.key]);
      let shown = ranked.slice(0, 12);
      const selectedRow = DATA.states.find((d) => d.name === selected);
      if (selectedRow && !shown.some((d) => d.name === selected)) shown = [...shown.slice(0, 11), selectedRow];
      const max = Math.max(...ranked.map((d) => d[spec.key]));
      shown.forEach((d) => {
        const row = document.createElement("button");
        row.type = "button"; row.className = "state-row";
        row.setAttribute("aria-current", String(d.name === selected));
        row.setAttribute("aria-label", `${d.label}: ${spec.format(d[spec.key])} ${spec.label}`);
        row.innerHTML = `<span class="state-name">${d.label}</span><span class="state-bar-track"><span class="state-bar" style="width:${Math.max(0.5, d[spec.key] / max * 100)}%"></span></span><span class="state-number">${spec.format(d[spec.key])}</span>`;
        row.addEventListener("click", () => { selected = d.name; select.value = selected; render(); });
        bars.append(row);
      });
      if (selectedRow) detail.innerHTML = `<strong>${selectedRow.label}</strong><span><b>${fmt.format(selectedRow.count)}</b> unresolved records</span><span><b>${selectedRow.rate.toFixed(1)}</b> per 100,000</span><span><b>${pct.format(selectedRow.confidential_share)}</b> confidential</span><span>Snapshot: 2 Dec 2025</span>`;
    }
    select.addEventListener("change", () => { selected = select.value; render(); });
    root.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => {
      metric = b.dataset.mode; buttonMode(root, metric); render();
    }));
    render();
  }

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
      clear(canvas);
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
      svg.append(svgNode("desc", {}, "Line showing total unresolved records, confidential records or confidential share across ten registry snapshots."));
      for (let i = 0; i <= 4; i++) {
        const v = ymin + (ymax - ymin) * i / 4, yy = y(v);
        svg.append(svgNode("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-grid" }));
        const tick = metric === "share"
          ? pct.format(v)
          : (v >= 1000 ? `${(v / 1000).toFixed(v >= 10000 ? 0 : 1)}k` : fmt.format(Math.round(v)));
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
        const html = `<strong>${d.snapshot}</strong><br>Total ${fmt.format(d.total)}<br>Confidential ${fmt.format(d.conf)}<br>Share ${pct.format(d.share)}`;
        c.setAttribute("aria-label", `${d.snapshot}: ${fmt.format(d.conf)} confidential of ${fmt.format(d.total)}`);
        c.addEventListener("mouseenter", (e) => {
          const [px, py] = pointerIn(e, canvas);
          showTip(tip, html, px, py);
        });
        c.addEventListener("mousemove", (e) => {
          const [px, py] = pointerIn(e, canvas);
          showTip(tip, html, px, py);
        });
        c.addEventListener("mouseleave", () => hideTip(tip));
        c.addEventListener("focus", () => showTip(tip, html, x(i), y(d[metric])));
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
  document.querySelectorAll('[data-chart="states"]').forEach(initStates);
  document.querySelectorAll('[data-chart="snapshots"]').forEach(initSnapshots);
})();
