/* Solar-sail drone simulator UI */
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
const S = { design: null, defaults: null, waypoints: [], commands: [], failures: null, job: null, mcJob: null,
            charts: {}, maps: {}, layers: {}, lastVoyage: null, lastMC: null };

async function api(path, body) {
  const r = await fetch(path, body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || r.statusText);
  return j;
}
const fmt = (v, d = 1) => (v === null || v === undefined || Number.isNaN(v)) ? "-" : Number(v).toFixed(d);
const getp = (o, p) => p.split(".").reduce((a, k) => a[k], o);
const setp = (o, p, v) => { const k = p.split("."); let a = o; for (let i = 0; i < k.length - 1; i++) a = a[k[i]]; a[k[k.length - 1]] = v; };
function download(name, obj) {
  const b = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = name; a.click();
}
function chart(id, cfg) {
  if (S.charts[id]) S.charts[id].destroy();
  cfg.options = Object.assign({ responsive: true, maintainAspectRatio: false, animation: false,
    plugins: { legend: { labels: { boxWidth: 10, font: { size: 11 } } } } }, cfg.options || {});
  S.charts[id] = new Chart(document.getElementById(id), cfg);
}
const COLORS = ["#1f5fa8", "#e07b39", "#2e8b57", "#8e44ad", "#c0392b", "#16a085", "#7f8c8d"];

/* ---------------- tabs ---------------- */
$$("nav button").forEach(b => b.onclick = () => {
  $$("nav button").forEach(x => x.classList.toggle("active", x === b));
  $$(".tab").forEach(t => t.classList.toggle("active", t.id === "tab-" + b.dataset.tab));
  setTimeout(() => Object.values(S.maps).forEach(m => m.invalidateSize()), 50);
});

/* ---------------- design ---------------- */
const GROUPS = { hull: "Hull", keel: "Keel", bulb: "Lead bulb", rudder: "Rudder", wing: "Wing sail", tail: "Tail",
                 power: "Power", comms: "Satellite comms", autopilot: "Autopilot" };
function buildSliders() {
  const host = $("#sliders"); host.innerHTML = "";
  const groups = {};
  for (const [path, label, mn, mx, step, unit] of S.defaults.editable) {
    const g = path.split(".")[0];
    if (!groups[g]) { const div = document.createElement("div"); div.className = "group"; div.innerHTML = `<h5>${GROUPS[g] || g}</h5>`; host.appendChild(div); groups[g] = div; }
    const v = getp(S.design, path);
    const row = document.createElement("div"); row.className = "slider";
    row.innerHTML = `<div class="name"><span>${label}</span><span class="unit">${unit}</span></div>
      <input type="range" min="${mn}" max="${mx}" step="${step}" value="${v}"><input type="number" min="${mn}" max="${mx}" step="${step}" value="${v}">`;
    const [r, n] = row.querySelectorAll("input");
    const upd = (val) => { r.value = val; n.value = val; setp(S.design, path, parseFloat(val)); scheduleAnalyze(); };
    r.oninput = () => upd(r.value); n.onchange = () => upd(n.value);
    groups[g].appendChild(row);
  }
  const tg = document.createElement("div"); tg.className = "group";
  tg.innerHTML = `<h5>Options</h5>
    <label class="check"><input type="checkbox" id="opt-buoy"> Wing core is buoyant (sealed foam)</label>
    <label class="check"><input type="checkbox" id="opt-bal"> Rig balanced by a counterweight</label>
    <label class="check"><input type="checkbox" id="opt-thr"> Thruster fitted</label>`;
  host.appendChild(tg);
  $("#opt-buoy").checked = S.design.wing.buoyant; $("#opt-bal").checked = S.design.wing.balanced;
  $("#opt-thr").checked = S.design.autopilot.thruster_policy.enabled;
  $("#opt-buoy").onchange = (e) => { S.design.wing.buoyant = e.target.checked; scheduleAnalyze(); };
  $("#opt-bal").onchange = (e) => { S.design.wing.balanced = e.target.checked; scheduleAnalyze(); };
  $("#opt-thr").onchange = (e) => { S.design.autopilot.thruster_policy.enabled = e.target.checked; scheduleAnalyze(); };
}
let anTimer = null;
function scheduleAnalyze() { clearTimeout(anTimer); anTimer = setTimeout(analyze, 700); }
async function analyze() {
  $("#design-busy").classList.remove("hidden");
  try {
    const r = await api("/api/analyze", { design: S.design });
    renderDesign(r);
  } catch (e) { $("#warnings").innerHTML = `<div class="w">Analysis failed: ${e.message}</div>`; }
  $("#design-busy").classList.add("hidden");
}
function card(k, v, s = "", cls = "") { return `<div class="card ${cls}"><div class="k">${k}</div><div class="v">${v}</div><div class="s">${s}</div></div>`; }
function renderDesign(r) {
  const s = r.summary, st = s.stability;
  $("#warnings").innerHTML = (s.warnings || []).map(w => `<div class="w">${w}</div>`).join("");
  $("#design-cards").innerHTML = [
    card("All-up mass", fmt(s.mass_kg, 1) + " kg", `ballast ${fmt(s.ballast_kg, 1)} kg (${fmt(100 * s.ballast_ratio, 0)}%)`),
    card("Waterline", fmt(s.waterline_z * 1000, 0) + " mm", `LWL ${fmt(s.lwl, 2)} m`),
    card("Stability (GM)", fmt(st.gm_m * 100, 1) + " cm", `max GZ ${fmt(st.max_gz_m * 100, 1)} cm at ${fmt(st.angle_max_gz, 0)} deg`),
    card("Self-righting", st.self_righting ? "Yes" : "No", `vanishing angle ${fmt(st.avs_deg, 0)} deg`, st.self_righting ? "good" : "bad"),
    card("Rig counterweight", fmt(s.counterweight_kg, 2) + " kg", `rig total ${fmt(s.rig_mass_kg, 2)} kg`, s.counterweight_kg > 1.5 ? "warn" : ""),
    card("Wing area", fmt(s.wing_area_m2, 2) + " m2", `buoyancy ${fmt(s.wing_buoyancy_kg, 1)} kg`),
    card("Wetted area", fmt(s.wetted_area_m2, 2) + " m2", `keel ${fmt(s.keel_area_m2 * 1e4, 0)} cm2`),
    card("Hardware cost", "$" + Math.round(s.cost.total).toLocaleString(), "estimate"),
  ].join("");
  drawBoat(r.outlines);
  const g = s.gz_curve;
  chart("ch-gz", { type: "line", data: { labels: g.angle, datasets: [{ label: "GZ (cm)", data: g.gz.map(v => v * 100), borderColor: COLORS[0], pointRadius: 0, fill: { target: "origin", above: "rgba(46,139,87,.12)", below: "rgba(192,57,43,.15)" } }] },
    options: { scales: { x: { title: { display: true, text: "heel (deg)" } }, y: { title: { display: true, text: "cm" } } } } });
  const twa = r.polar.twa;
  const ds = Object.entries(r.polar.kn).map(([tws, arr], i) => ({ label: `${tws} m/s`, borderColor: COLORS[i], showLine: true, pointRadius: 0,
    data: arr.map((u, k) => ({ x: Math.max(u, 0) * Math.sin(twa[k] * Math.PI / 180), y: Math.max(u, 0) * Math.cos(twa[k] * Math.PI / 180) })) }));
  chart("ch-polar", { type: "scatter", data: { datasets: ds }, options: { aspectRatio: 1, scales: { x: { min: 0, title: { display: true, text: "knots (wind from top)" } }, y: {} } } });
  $("#tbl-mass").innerHTML = "<tr><th>Item</th><th>kg</th><th>x</th><th>z</th></tr>" +
    s.mass_items.map(([n, m, p]) => `<tr><td>${n}</td><td>${fmt(m, 2)}</td><td>${fmt(p[0], 2)}</td><td>${fmt(p[2], 2)}</td></tr>`).join("");
  $("#tbl-cost").innerHTML = "<tr><th>Item</th><th>USD</th></tr>" + Object.entries(s.cost.items).map(([k, v]) => `<tr><td>${k}</td><td>${Math.round(v)}</td></tr>`).join("") +
    `<tr><th>Total</th><th>${Math.round(s.cost.total)}</th></tr>`;
}
function drawBoat(o) {
  const svg = $("#profile-svg"); const W = svg.clientWidth || 600, H = svg.clientHeight || 300;
  const all = [].concat(o.profile, o.fin, o.bulb, o.rudder, o.wing, o.tail);
  const xs = all.map(p => p[0]), zs = all.map(p => p[1]);
  const x0 = Math.min(...xs) - 0.1, x1 = Math.max(...xs) + 0.15, z0 = Math.min(...zs) - 0.05, z1 = Math.max(...zs) + 0.05;
  const sc = Math.min(W / (x1 - x0), H / (z1 - z0));
  const X = x => (x - x0) * sc + (W - (x1 - x0) * sc) / 2, Z = z => H - ((z - z0) * sc + (H - (z1 - z0) * sc) / 2);
  const poly = (pts, st) => `<polygon points="${pts.map(p => `${X(p[0])},${Z(p[1])}`).join(" ")}" ${st}/>`;
  const line = (pts, st) => `<polyline points="${pts.map(p => `${X(p[0])},${Z(p[1])}`).join(" ")}" fill="none" ${st}/>`;
  svg.innerHTML = `
    <line x1="0" x2="${W}" y1="${Z(o.waterline)}" y2="${Z(o.waterline)}" stroke="#3b8bd4" stroke-width="1"/>
    ${poly(o.profile, 'fill="#e8eef6" stroke="#1b1f24"')}${poly(o.fin, 'fill="#f4f6f8" stroke="#1b1f24"')}
    ${poly(o.bulb, 'fill="#666" stroke="#1b1f24"')}${poly(o.rudder, 'fill="#f4f6f8" stroke="#1b1f24"')}
    ${poly(o.wing, 'fill="rgba(31,95,168,.08)" stroke="#1f5fa8"')}${poly(o.tail, 'fill="rgba(31,95,168,.08)" stroke="#1f5fa8"')}
    ${line(o.boom, 'stroke="#1f5fa8" stroke-width="2"')}${line(o.counterweight_arm, 'stroke="#e07b39" stroke-width="2"')}
    <circle cx="${X(o.cg[0])}" cy="${Z(o.cg[2])}" r="4" fill="#c0392b"/><text x="${X(o.cg[0]) + 6}" y="${Z(o.cg[2]) + 4}" font-size="11" fill="#c0392b">CG</text>
    <text x="6" y="14" font-size="11" fill="#5f6b78">Side view (bow left), to scale</text>`;
  const sv = $("#plan-svg"); const W2 = sv.clientWidth || 400, H2 = sv.clientHeight || 300;
  const px = o.plan.map(p => p[0]), py = o.plan.map(p => p[1]);
  const sc2 = Math.min(W2 / (Math.max(...px) + 0.2), H2 / (2 * Math.max(...py) + 0.4));
  const X2 = x => (x + 0.1) * sc2, Y2 = y => H2 / 2 - y * sc2;
  sv.innerHTML = `<polygon points="${o.plan.map(p => `${X2(p[0])},${Y2(p[1])}`).join(" ")}" fill="#e8eef6" stroke="#1b1f24"/>
    <line x1="${X2(0)}" x2="${X2(o.length)}" y1="${H2 / 2}" y2="${H2 / 2}" stroke="#aaa" stroke-dasharray="4 3"/>
    <circle cx="${X2(o.wing[0][0] + (o.boom[0][0] - o.wing[0][0]))}" cy="${H2 / 2}" r="5" fill="none" stroke="#1f5fa8"/>
    <text x="6" y="14" font-size="11" fill="#5f6b78">Plan view</text>`;
}
$("#btn-analyze").onclick = analyze;
$("#btn-reset").onclick = () => { S.design = structuredClone(S.defaults.design); buildSliders(); analyze(); };
$("#btn-dl-design").onclick = () => download((S.design.name || "design").replace(/\W+/g, "_") + ".json", S.design);
$("#in-design").onchange = async (e) => {
  const f = e.target.files[0]; if (!f) return;
  const d = JSON.parse(await f.text());
  S.design = Object.assign(structuredClone(S.defaults.design), d.design || d);
  for (const k of Object.keys(S.defaults.design)) if (typeof S.defaults.design[k] === "object" && S.defaults.design[k] !== null && !Array.isArray(S.defaults.design[k])) S.design[k] = Object.assign(structuredClone(S.defaults.design[k]), (d.design || d)[k] || {});
  buildSliders(); analyze();
};
$("#in-mesh").onchange = async (e) => {
  const f = e.target.files[0]; if (!f) return;
  const q = new URLSearchParams({ name: f.name, role: $("#mesh-role").value, units: $("#mesh-units").value, axes: $("#mesh-axes").value });
  $("#mesh-info").textContent = "Uploading ...";
  const r = await fetch("/api/upload_mesh?" + q, { method: "POST", body: await f.arrayBuffer() }).then(r => r.json());
  if (r.error) { $("#mesh-info").textContent = r.error; return; }
  const spec = r.spec; const m = parseFloat($("#mesh-mass").value); if (m) spec.mass_kg = m;
  S.design.hull.stl = spec;
  $("#mesh-info").innerHTML = `Loaded ${r.info.triangles.toLocaleString()} triangles, size ${r.extent_m.map(v => v.toFixed(2)).join(" x ")} m, ` +
    (r.info.watertight ? "watertight" : `<b>not watertight (${r.info.open_edges} open edges)</b>`);
  analyze();
};
$("#btn-clear-mesh").onclick = () => { S.design.hull.stl = null; $("#mesh-info").textContent = "Using the parametric hull."; analyze(); };

/* ---------------- scenario ---------------- */
function initScenarioMap() {
  const m = L.map("map-scn", { worldCopyJump: true }).setView([50, -30], 3);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap" }).addTo(m);
  S.maps.scn = m; S.mapMode = "start";
  S.layers.start = L.circleMarker([0, 0], { radius: 7, color: "#2e8b57", fillOpacity: .9 }).addTo(m);
  S.layers.target = L.circleMarker([0, 0], { radius: 7, color: "#c0392b", fillOpacity: .9 }).addTo(m);
  S.layers.route = L.polyline([], { color: "#1f5fa8", dashArray: "6 6" }).addTo(m);
  m.on("click", (e) => {
    const lat = +e.latlng.lat.toFixed(3), lon = +(((e.latlng.lng + 540) % 360) - 180).toFixed(3);
    if (S.mapMode === "start") { $("#s-lat").value = lat; $("#s-lon").value = lon; }
    else if (S.mapMode === "target") { $("#t-lat").value = lat; $("#t-lon").value = lon; }
    else S.waypoints.push([lat, lon]);
    updateRoute();
  });
}
function updateRoute() {
  const s = [+$("#s-lat").value, +$("#s-lon").value], t = [+$("#t-lat").value, +$("#t-lon").value];
  S.layers.start.setLatLng(s); S.layers.target.setLatLng(t);
  S.layers.route.setLatLngs([s, ...S.waypoints, t]);
}
$$(".mapmode").forEach(b => b.onclick = () => { $$(".mapmode").forEach(x => x.classList.toggle("active", x === b)); S.mapMode = b.dataset.mode; });
$("#btn-clear-wp").onclick = () => { S.waypoints = []; updateRoute(); };
["#s-lat", "#s-lon", "#t-lat", "#t-lon"].forEach(id => $(id).onchange = updateRoute);
const MA_WP = [[42.0, -48.0]];   // south of the Grand Banks
const PRESETS = { ocmd: { s: [38.25, -74.65], t: [51.35, -9.7], w: MA_WP, time: "2024-05-15T12:00" },
                  vab: { s: [36.85, -75.55], t: [51.35, -9.7], w: MA_WP, time: "2024-05-15T12:00" },
                  cm: { s: [38.75, -74.55], t: [51.35, -9.7], w: MA_WP, time: "2024-05-15T12:00" },
                  ocbr: { s: [38.25, -74.65], t: [48.6, -5.6], w: MA_WP, time: "2024-05-15T12:00" },
                  ocpt: { s: [38.25, -74.65], t: [39.4, -9.6], w: [[39.5, -45.0]], time: "2024-05-15T12:00" },
                  nf: { s: [47.3, -52.3], t: [53.3, -10.2], time: "2024-06-10T12:00" },
                  ca: { s: [27.9, -15.3], t: [13.1, -59.4], time: "2024-05-07T12:00" } };
$("#preset").onchange = (e) => { const p = PRESETS[e.target.value]; if (!p) return;
  $("#s-lat").value = p.s[0]; $("#s-lon").value = p.s[1]; $("#t-lat").value = p.t[0]; $("#t-lon").value = p.t[1]; $("#s-time").value = p.time;
  S.waypoints = (p.w || []).map(w => w.slice()); updateRoute(); S.maps.scn.fitBounds([p.s, p.t], { padding: [40, 40] }); };
$("#s-mode").onchange = () => {
  const six = $("#s-mode").value === "6dof";
  const days = +$("#s-days").value || 1, dt = +$("#s-dt6").value;
  $("#sixdof-note").classList.toggle("hidden", !six);
  $("#sixdof-note").textContent = `Full 6-DOF integrates every ${dt} s: expect roughly ${fmt(0.5 * 0.05 / dt, 2)} h of computer time per simulated day ` +
    `(about ${fmt(days * 0.5 * 0.05 / dt, 0)} h for ${days} days). Use it for storms or a few days; use Hybrid for whole crossings and Monte Carlo.`;
};
$("#s-days").onchange = () => $("#s-mode").onchange(); $("#s-dt6").onchange = () => $("#s-mode").onchange();
function buildFailures() {
  $("#tbl-fail").innerHTML = "<tr><th>On</th><th>Hazard</th><th>Rate/day</th><th>Notes</th></tr>" +
    Object.entries(S.failures).map(([k, v]) => `<tr><td><input type="checkbox" data-f="${k}" ${v.enabled ? "checked" : ""}></td><td>${k.replace(/_/g, " ")}</td>
      <td><input type="number" step="any" data-r="${k}" value="${v.per_day}"></td><td class="hint">${v.note}</td></tr>`).join("");
  $$("#tbl-fail input[data-f]").forEach(i => i.onchange = () => S.failures[i.dataset.f].enabled = i.checked);
  $$("#tbl-fail input[data-r]").forEach(i => i.onchange = () => S.failures[i.dataset.r].per_day = parseFloat(i.value));
}
function buildCommands() {
  $("#tbl-cmd").innerHTML = "<tr><th>Day</th><th>Command</th><th>Args</th><th></th></tr>" +
    S.commands.map((c, i) => `<tr><td>${fmt(c.t_hours / 24, 2)}</td><td>${c.cmd}</td><td>${JSON.stringify(c.args)}</td><td><button class="small" data-del="${i}">x</button></td></tr>`).join("");
  $$("#tbl-cmd button[data-del]").forEach(b => b.onclick = () => { S.commands.splice(+b.dataset.del, 1); buildCommands(); });
}
const CMD_HINTS = { SET_REPORT: '{"hours": 1}', GOTO: '{"lat": 52, "lon": -12}', SET_ROUTE: '{"waypoints": [[50,-30],[53,-12]]}',
  MODE: '{"mode": "sail"}  (sail, sail+thrust, station, drift, safe)', THRUSTER_POLICY: '{"enabled": true, "min_soc": 0.7, "max_hours_per_day": 2}',
  GEOFENCE: '{"lat": 50, "lon": -20, "radius_km": 100}', DIAG: "{}", REBOOT: "{}" };
$("#cmd-type").onchange = () => $("#cmd-args").placeholder = CMD_HINTS[$("#cmd-type").value];
$("#btn-add-cmd").onclick = () => {
  let args = {}; try { args = JSON.parse($("#cmd-args").value || "{}"); } catch (e) { alert("Args must be JSON"); return; }
  S.commands.push({ t_hours: (+$("#cmd-day").value || 0) * 24, cmd: $("#cmd-type").value, args });
  S.commands.sort((a, b) => a.t_hours - b.t_hours); buildCommands();
};
function scenario() {
  return { start: { lat: +$("#s-lat").value, lon: +$("#s-lon").value }, target: { lat: +$("#t-lat").value, lon: +$("#t-lon").value },
    waypoints: S.waypoints, atlantic_islands_count: $("#s-isles").checked, start_time: $("#s-time").value + ":00", max_days: +$("#s-days").value, provider: $("#s-provider").value,
    grid_deg: +$("#s-grid").value, fine_grid: $("#s-fine").checked ? (S.defaults.scenario.fine_grid || { deg: 0.25, lat: [30, 50], lon: [-80, -38] }) : null, arrival_radius_km: +$("#s-radius").value, seed: +$("#s-seed").value, mode: $("#s-mode").value,
    dt_s: +$("#s-dt").value, dt_6dof_s: +$("#s-dt6").value, log_interval_min: +$("#s-log").value,
    failures_enabled: $("#s-fail").checked, failures: S.failures, commands: S.commands };
}
function fillScenario(sc) {
  $("#s-lat").value = sc.start.lat; $("#s-lon").value = sc.start.lon; $("#t-lat").value = sc.target.lat; $("#t-lon").value = sc.target.lon;
  $("#s-time").value = sc.start_time.slice(0, 16); $("#s-days").value = sc.max_days; $("#s-provider").value = sc.provider;
  $("#s-radius").value = sc.arrival_radius_km; $("#s-seed").value = sc.seed; $("#s-mode").value = sc.mode; $("#s-dt").value = sc.dt_s;
  $("#s-log").value = sc.log_interval_min; $("#s-fail").checked = sc.failures_enabled;
  S.waypoints = (sc.waypoints || []).map(w => w.slice()); $("#s-isles").checked = !!sc.atlantic_islands_count;
  $("#s-grid").value = String(sc.grid_deg); $("#s-fine").checked = !!sc.fine_grid;
}

/* ---------------- run ---------------- */
async function poll(id, onUpdate, onDone) {
  let logN = 0;
  const tick = async () => {
    let j; try { j = await api(`/api/job/${id}?log=${logN}`); } catch (e) { setTimeout(tick, 2000); return; }
    logN = j.log_total; onUpdate(j);
    if (j.status === "done") onDone(j.result);
    else if (j.status === "error" || j.status === "cancelled") onDone(null, j);
    else setTimeout(tick, 1000);
  };
  tick();
}
function initRunMap(id) {
  const m = L.map(id, { worldCopyJump: true }).setView([50, -30], 3);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap" }).addTo(m);
  return m;
}
$("#btn-run").onclick = async () => {
  $("#log").textContent = ""; $("#btn-export").disabled = true;
  const sc = scenario();
  try {
    const { id } = await api("/api/run", { design: S.design, scenario: sc });
    S.job = id;
    const live = L.circleMarker([sc.start.lat, sc.start.lon], { radius: 6, color: "#e07b39" }).addTo(S.maps.run);
    poll(id, (j) => {
      $("#prog-bar").style.width = (100 * j.progress) + "%"; $("#prog-txt").textContent = `${j.status} ${fmt(100 * j.progress, 0)}%  (${fmt(j.elapsed, 0)} s)`;
      if (j.logs.length) $("#log").textContent += j.logs.join("\n") + "\n";
      if (j.live && j.live.lat) live.setLatLng([j.live.lat, j.live.lon]);
    }, (res, j) => {
      S.maps.run.removeLayer(live);
      if (!res) { $("#prog-txt").textContent = j.status + (j.error ? ": " + j.error : ""); return; }
      $("#btn-export").disabled = false; renderVoyage(res);
    });
  } catch (e) { alert(e.message); }
};
$("#btn-cancel").onclick = () => S.job && api(`/api/job/${S.job}/cancel`, {});
$("#btn-export").onclick = () => S.job && (window.location = `/api/export/${S.job}`);
$("#in-results").onchange = async (e) => {
  const f = e.target.files[0]; if (!f) return;
  const d = JSON.parse(await f.text());
  if (d.kind === "montecarlo") { $$("nav button")[3].click(); renderMC(d.result); } else renderVoyage(d.result || d);
};
const OUTCOME_TXT = { arrived_reporting: "Arrived, reporting", arrived_silent: "Arrived, silent", at_sea_timeout: "Still at sea", aground: "Aground", lost: "Lost" };
function renderVoyage(r) {
  S.lastVoyage = r;
  const good = r.outcome === "arrived_reporting";
  $("#run-summary").innerHTML = [
    card("Outcome", OUTCOME_TXT[r.outcome] || r.outcome, r.failures.length ? r.failures[r.failures.length - 1].msg : "", good ? "good" : (r.outcome.startsWith("arrived") ? "warn" : "bad")),
    card("Duration", fmt(r.days, 1) + " days", `${fmt(r.distance_km, 0)} km sailed`),
    card("Average speed", fmt(r.stats.mean_sog_kn, 2) + " kn", `max wind ${fmt(r.stats.max_tws_ms, 0)} m/s, max Hs ${fmt(r.stats.max_hs_m, 1)} m`),
    card("Satellite cost", "$" + fmt(r.airtime_usd, 0), `${r.sessions_ok} reports, ${r.sessions_failed} failed`),
    card("Knockdowns", r.knockdowns, `capsizes ${r.capsizes}`),
    card("Battery", fmt(100 * r.final_soc, 0) + "% at end", `min ${fmt(100 * r.stats.min_soc, 0)}%`),
  ].join("");
  const ser = r.series, m = S.maps.run;
  if (S.layers.run) m.removeLayer(S.layers.run);
  const g = L.layerGroup().addTo(m); S.layers.run = g;
  const maxS = Math.max(...ser.map(s => s.sog), 0.5);
  for (let i = 1; i < ser.length; i++) {
    const t = Math.min(ser[i].sog / maxS, 1);
    const col = `hsl(${220 - 200 * t},70%,45%)`;
    L.polyline([[ser[i - 1].lat, ser[i - 1].lon], [ser[i].lat, ser[i].lon]], { color: col, weight: 3 }).addTo(g);
  }
  L.circleMarker([ser[0].lat, ser[0].lon], { radius: 7, color: "#2e8b57", fillOpacity: 1 }).bindTooltip("Start").addTo(g);
  L.circleMarker([r.end.lat, r.end.lon], { radius: 7, color: good ? "#2e8b57" : "#c0392b", fillOpacity: 1 }).bindTooltip(OUTCOME_TXT[r.outcome]).addTo(g);
  for (const ev of r.events) {
    if (!["failure", "arrival", "knockdown", "alarm"].includes(ev.kind)) continue;
    const s = ser.reduce((a, b) => Math.abs(b.t - ev.day * 24) < Math.abs(a.t - ev.day * 24) ? b : a, ser[0]);
    L.circleMarker([s.lat, s.lon], { radius: ev.kind === "knockdown" ? 3 : 6, color: ev.kind === "failure" ? "#c0392b" : ev.kind === "arrival" ? "#2e8b57" : "#e07b39" })
      .bindTooltip(`Day ${fmt(ev.day, 1)}: ${ev.msg}`).addTo(g);
  }
  m.fitBounds(L.latLngBounds(ser.map(s => [s.lat, s.lon])), { padding: [30, 30] });
  const x = ser.map(s => s.t / 24);
  const ds = (label, data, color, axis = "y", extra = {}) => Object.assign({ label, data: data.map((v, i) => ({ x: x[i], y: v })), borderColor: color, pointRadius: 0, borderWidth: 1.2, yAxisID: axis }, extra);
  const xopt = { type: "linear", title: { display: true, text: "day" } };
  chart("ch-speed", { type: "line", data: { datasets: [ds("speed over ground (kn)", ser.map(s => s.sog * 1.944), COLORS[0]), ds("true wind (m/s)", ser.map(s => s.tws), COLORS[1], "y2")] },
    options: { scales: { x: xopt, y: { title: { display: true, text: "kn" } }, y2: { position: "right", grid: { display: false }, title: { display: true, text: "m/s" } } } } });
  chart("ch-waves", { type: "line", data: { datasets: [ds("Hs (m)", ser.map(s => s.hs), COLORS[2]), ds("heel (deg)", ser.map(s => s.heel), COLORS[4], "y2")] },
    options: { scales: { x: xopt, y: { title: { display: true, text: "m" } }, y2: { position: "right", grid: { display: false } } } } });
  chart("ch-power", { type: "line", data: { datasets: [ds("battery (%)", ser.map(s => 100 * s.soc), COLORS[0]), ds("solar (W)", ser.map(s => s.solar_w), COLORS[1], "y2")] },
    options: { scales: { x: xopt, y: { min: 0, max: 100 }, y2: { position: "right", grid: { display: false } } } } });
  chart("ch-cur", { type: "line", data: { datasets: [ds("current (kn)", ser.map(s => s.cur * 1.944), COLORS[5]), ds("sea level incl. tide (m)", ser.map(s => s.sea_level), COLORS[3], "y2")] },
    options: { scales: { x: xopt, y: {}, y2: { position: "right", grid: { display: false } } } } });
  $("#tbl-events").innerHTML = "<tr><th>Day</th><th>Type</th><th>Event</th></tr>" + r.events.filter(e => e.kind !== "nav" || r.events.length < 400)
    .map(e => `<tr><td>${fmt(e.day, 2)}</td><td>${e.kind}</td><td>${e.msg}</td></tr>`).join("");
}

/* ---------------- monte carlo ---------------- */
$("#btn-mc").onclick = async () => {
  const yrs = $("#mc-years").value.split(",").map(s => s.trim()).filter(Boolean).map(Number);
  const mc = { n_runs: +$("#mc-n").value, processes: +$("#mc-proc").value || null,
    window: $("#mc-from").value ? { from: $("#mc-from").value + "T12:00:00", to: ($("#mc-to").value || $("#mc-from").value) + "T12:00:00", years: yrs } : null };
  const sc = scenario(); if (sc.mode === "6dof" && !confirm("Monte Carlo with the full 6-DOF model will take a very long time. Continue?")) return;
  $("#log").textContent = "";
  const { id } = await api("/api/montecarlo", { design: S.design, scenario: sc, mc });
  S.mcJob = id; $("#btn-mc-export").disabled = true;
  poll(id, (j) => { $("#mc-bar").style.width = (100 * j.progress) + "%";
    $("#mc-txt").textContent = `${j.status} ${j.live ? j.live.done + "/" + mc.n_runs : ""} (${fmt(j.elapsed, 0)} s) ${j.logs.length ? j.logs[j.logs.length - 1].slice(10) : ""}`; },
    (res, j) => { if (!res) { $("#mc-txt").textContent = j.status + (j.error ? ": " + j.error : ""); return; } $("#btn-mc-export").disabled = false; renderMC(res); });
};
$("#btn-mc-cancel").onclick = () => S.mcJob && api(`/api/job/${S.mcJob}/cancel`, {});
$("#btn-mc-export").onclick = () => S.mcJob && (window.location = `/api/export/${S.mcJob}`);
const OC_COL = { arrived_reporting: "#2e8b57", arrived_silent: "#8fbf6f", at_sea_timeout: "#b7791f", aground: "#8e44ad", lost: "#c0392b" };
function renderMC(r) {
  S.lastMC = r; const s = r.summary;
  $("#mc-cards").innerHTML = [
    card("Reaches Europe, still reporting", fmt(s.success_percent, 0) + "%", `95% range ${s.success_ci95[0]}-${s.success_ci95[1]}% (${s.runs} runs)`, "good"),
    card("Reaches Europe at all", fmt(s.any_arrival_percent, 0) + "%", "including silent arrivals"),
    card("Median crossing", s.arrival_days.median ? fmt(s.arrival_days.median, 0) + " days" : "-", s.arrival_days.p10 ? `10-90%: ${fmt(s.arrival_days.p10, 0)}-${fmt(s.arrival_days.p90, 0)} days` : ""),
    card("Lost", fmt(s.percent.lost, 0) + "%", `aground ${fmt(s.percent.aground, 0)}%, still at sea ${fmt(s.percent.at_sea_timeout, 0)}%`, "bad"),
    card("Satellite cost", "$" + fmt(s.mean_airtime_usd, 0), "mean per voyage"),
    card("Knockdowns", fmt(s.mean_knockdowns, 1), "mean per voyage"),
  ].join("");
  chart("ch-outcomes", { type: "bar", data: { labels: Object.keys(s.counts).map(k => OUTCOME_TXT[k]), datasets: [{ label: "runs", data: Object.values(s.counts), backgroundColor: Object.keys(s.counts).map(k => OC_COL[k]) }] },
    options: { plugins: { legend: { display: false } } } });
  const days = s.arrival_days.all || []; const bins = {};
  days.forEach(d => { const b = Math.floor(d / 5) * 5; bins[b] = (bins[b] || 0) + 1; });
  const keys = Object.keys(bins).map(Number).sort((a, b) => a - b);
  chart("ch-days", { type: "bar", data: { labels: keys.map(k => `${k}-${k + 5}`), datasets: [{ label: "arrivals", data: keys.map(k => bins[k]), backgroundColor: "#1f5fa8" }] },
    options: { plugins: { legend: { display: false } } } });
  chart("ch-causes", { type: "bar", data: { labels: Object.keys(s.failure_causes), datasets: [{ label: "runs", data: Object.values(s.failure_causes), backgroundColor: "#c0392b" }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } } } });
  const bm = s.by_launch_month || {}; const MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const mk = Object.keys(bm).sort();
  chart("ch-months", { type: "bar", data: { labels: mk.map(k => `${MN[+k - 1]} (${bm[k].runs})`), datasets: [
      { type: "bar", label: "95% range", data: mk.map(k => bm[k].success_ci95), backgroundColor: "rgba(31,95,168,.18)", barPercentage: 0.35 },
      { type: "line", label: "reaches Europe reporting (%)", data: mk.map(k => bm[k].success_percent), showLine: false, pointRadius: 5, borderColor: "#1f5fa8", backgroundColor: "#1f5fa8" }] },
    options: { scales: { y: { min: 0, max: 100, title: { display: true, text: "%" } } }, plugins: { legend: { display: false } } } });
  const m = S.maps.mc; if (S.layers.mc) m.removeLayer(S.layers.mc);
  const g = L.layerGroup().addTo(m); S.layers.mc = g; const pts = [];
  for (const run of r.runs) { if (!run.track) continue;
    L.polyline(run.track, { color: OC_COL[run.outcome] || "#888", weight: 1.2, opacity: .55 }).bindTooltip(`Run ${run.i}: ${OUTCOME_TXT[run.outcome]}, ${fmt(run.days, 0)} d`).addTo(g);
    pts.push(...run.track); }
  if (pts.length) m.fitBounds(L.latLngBounds(pts), { padding: [20, 20] });
  $("#tbl-runs").innerHTML = "<tr><th>#</th><th>Start</th><th>Outcome</th><th>Days</th><th>km</th><th>Cost</th><th>What happened</th></tr>" +
    r.runs.map(x => `<tr><td>${x.i}</td><td>${(x.start_time || "").slice(0, 10)}</td><td style="color:${OC_COL[x.outcome]}">${OUTCOME_TXT[x.outcome] || x.error}</td>
      <td>${fmt(x.days, 1)}</td><td>${fmt(x.distance_km, 0)}</td><td>$${fmt(x.airtime_usd, 0)}</td><td>${(x.failures || []).join("; ")}</td></tr>`).join("");
}

/* ---------------- boot ---------------- */
(async function boot() {
  S.defaults = await api("/api/defaults");
  S.design = structuredClone(S.defaults.design); S.failures = structuredClone(S.defaults.failures);
  buildSliders(); buildFailures(); buildCommands();
  initScenarioMap(); fillScenario(S.defaults.scenario); updateRoute(); $("#s-mode").onchange();
  S.maps.run = initRunMap("map-run"); S.maps.mc = initRunMap("map-mc");
  $("#mc-proc").value = Math.max(1, (S.defaults.cpu || 2) - 1);
  $("#mc-from").value = "2022-06-01"; $("#mc-to").value = "2022-06-30"; $("#mc-years").value = "2022,2023,2024,2025";
  $("#cmd-type").onchange();
  analyze();
})();
