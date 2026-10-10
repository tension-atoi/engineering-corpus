/* GNU6 identity rig — runtime (vanilla, no dependencies).
 *
 * State is ONE scalar t (units of 120deg). Rest poses are integer t (0 blue, 1 green, 2 orange, mod 3).
 * Rotation, face colours and the glyph morph are pure functions of t, so interruption cannot contaminate
 * state and an integer t always renders the exact rest pose.
 */
(() => {
  "use strict";
  const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const mod3 = (n) => ((n % 3) + 3) % 3;
  // Policy comes from the embedding surface; native reduced-motion remains a hard floor.
  // A local GNU6 Off selection must not leave the rig spring running.
  const NS = "http://www.w3.org/2000/svg";
  const VS = "attribute vec2 p;attribute vec2 u;varying vec2 uv;void main(){uv=u;gl_Position=vec4(p,0,1);}";
  const FS = `precision mediump float;varying vec2 uv;uniform sampler2D tex;uniform vec3 w;uniform vec3 col;uniform float aa;uniform float range;
    void main(){vec3 s=texture2D(tex,uv).rgb-.5;float d=dot(s,w)*2.*range;float a=smoothstep(-aa,aa,d);gl_FragColor=vec4(col*a,a);}`;

  function create(host, data, opts = {}) {
    const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches || opts.shouldSnap?.() === true;
    const [W] = [1254], C = data.centre, G = data.glyph, A = G.anchors;
    const rot = (p, deg) => { const a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); const x = p[0] - C[0], y = p[1] - C[1]; return [C[0] + x * c - y * s, C[1] + x * s + y * c]; };
    const corr = A.map((a, k) => { const r = rot(A[0], 120 * k); return [a[0] - r[0], a[1] - r[1]]; });
    host.classList.add("g6-rig"); host.style.position = "relative"; host.style.aspectRatio = "1"; host.innerHTML = "";
    host.setAttribute("role", "img"); host.setAttribute("aria-label", opts.label || "gnu6 identity");
    const svg = document.createElementNS(NS, "svg"); svg.setAttribute("viewBox", `0 0 ${W} ${W}`); svg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;overflow:visible";
    const uid = "rg" + Math.random().toString(36).slice(2, 7), defs = document.createElementNS(NS, "defs"), grp = document.createElementNS(NS, "g");
    svg.append(defs, grp);
    const faces = Object.keys(data.faces).map((slot) => {
      const g = document.createElementNS(NS, "linearGradient"); g.setAttribute("id", `${uid}-${slot}`); g.setAttribute("gradientUnits", "userSpaceOnUse");
      const stops = data.grad[slot][0].stops.map((s) => { const e = document.createElementNS(NS, "stop"); e.setAttribute("offset", s[0]); g.append(e); return e; });
      defs.append(g);
      const p = document.createElementNS(NS, "path"); p.setAttribute("d", data.faces[slot]); p.setAttribute("fill", `url(#${uid}-${slot})`); p.setAttribute("transform", `translate(0 ${W}) scale(1 -1)`); grp.append(p);
      return { slot, g, stops, poses: data.grad[slot] };
    });
    host.append(svg);
    const cv = document.createElement("canvas"); cv.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none"; cv.setAttribute("aria-hidden", "true"); host.append(cv);
    const gl = opts.noWebGL ? null : cv.getContext("webgl", { premultipliedAlpha: true, alpha: true, antialias: false });
    // no-WebGL path: vector glyphs, swapped at the half-way point of a turn (a swap, never a fade)
    let fb = null;
    if (!gl && G.paths) {
      fb = document.createElementNS(NS, "path"); fb.setAttribute("fill", `rgb(${G.color.join(",")})`); svg.append(fb);
      host.dataset.rigGlyph = "vector";
    } else host.dataset.rigGlyph = "webgl";
    let ready = false, prog, loc = {};
    if (gl) {
      const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; };
      prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog); gl.useProgram(prog);
      const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
      const ap = gl.getAttribLocation(prog, "p"), au = gl.getAttribLocation(prog, "u");
      gl.enableVertexAttribArray(ap); gl.vertexAttribPointer(ap, 2, gl.FLOAT, false, 16, 0);   // clip position
      gl.enableVertexAttribArray(au); gl.vertexAttribPointer(au, 2, gl.FLOAT, false, 16, 8);   // crop-local texture coordinate
      for (const n of ["tex", "w", "col", "aa", "range"]) loc[n] = gl.getUniformLocation(prog, n);
      const img = new Image(); img.onload = () => {
        const tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
        for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
        ready = true; render(); host.dispatchEvent(new CustomEvent("g6rig:ready"));
      };
      img.src = opts.sdf || "glyph-sdf.png";
    }

    // ── state: one scalar and its spring
    const S = { t: opts.t0 || 0, v: 0, target: opts.t0 || 0, lean: 0, leanV: 0, leanTarget: 0, breath: 0, breathUntil: 0, ambient: false, running: false, last: 0, id: 0 };
    const lerp = (a, b, x) => a + (b - a) * x;
    function render() {
      const te = S.t + S.lean + S.breath;
      const n = Math.floor(te), f = te - n, a = mod3(n), b = mod3(n + 1);
      grp.setAttribute("transform", `rotate(${120 * te} ${C[0]} ${C[1]})`);
      const fc = smooth(0, 0.8, f);                                                  // colour leads the glyph
      for (const F of faces) {
        const pa = F.poses[a], pb = F.poses[b];
        F.g.setAttribute("x1", lerp(pa.q0[0], pb.q0[0], fc)); F.g.setAttribute("y1", lerp(pa.q0[1], pb.q0[1], fc));
        F.g.setAttribute("x2", lerp(pa.q1[0], pb.q1[0], fc)); F.g.setAttribute("y2", lerp(pa.q1[1], pb.q1[1], fc));
        F.stops.forEach((e, i) => { const ca = pa.stops[i][1], cb = pb.stops[i][1]; e.setAttribute("stop-color", `rgb(${lerp(ca[0], cb[0], fc).toFixed(1)},${lerp(ca[1], cb[1], fc).toFixed(1)},${lerp(ca[2], cb[2], fc).toFixed(1)})`); });
      }
      if (fb) {
        const k = f < 0.5 ? a : b, base0 = rot(A[0], 120 * te), ck = [lerp(corr[a][0], corr[b][0], f), lerp(corr[a][1], corr[b][1], f)];
        const px = base0[0] + ck[0] - A[k][0], py = base0[1] + ck[1] - A[k][1];
        if (fb.dataset.k !== String(k)) { fb.setAttribute("d", G.paths[k]); fb.dataset.k = String(k); }
        fb.setAttribute("transform", `translate(${px.toFixed(2)} ${py.toFixed(2)}) translate(0 ${W}) scale(1 -1)`);
        return;
      }
      if (!gl || !ready) return;
      const px = Math.max(1, Math.round(host.clientWidth * Math.min(devicePixelRatio || 1, 2)));
      if (cv.width !== px) { cv.width = px; cv.height = px; }
      gl.viewport(0, 0, px, px); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      const base = rot(A[0], 120 * te), ca = corr[a], cb = corr[b], fg = smooth(0.3, 0.9, f);
      const p = [base[0] + lerp(ca[0], cb[0], f), base[1] + lerp(ca[1], cb[1], f)];   // glyph follows its face; per-identity offsets fade in
      // quad = crop square centred on p, mapped into canvas clip space
      const s = G.crop / W, cx = p[0] / W, cy = p[1] / W, x0 = cx - s / 2, x1 = cx + s / 2, y0 = cy - s / 2, y1 = cy + s / 2;
      const X = (v) => v * 2 - 1, Y = (v) => 1 - v * 2;                                // cube-space fraction -> clip space (y down in the image)
      const q = new Float32Array([X(x0), Y(y0), 0, 0,  X(x1), Y(y0), 1, 0,  X(x0), Y(y1), 0, 1,  X(x1), Y(y1), 1, 1]);   // TL TR BL BR with uv, row 0 = top
      gl.bufferData(gl.ARRAY_BUFFER, q, gl.DYNAMIC_DRAW);
      const w = [0, 0, 0]; w[a] += 1 - fg; w[b] += fg;
      gl.uniform1i(loc.tex, 0); gl.uniform3f(loc.w, w[0], w[1], w[2]); gl.uniform3f(loc.col, G.color[0] / 255, G.color[1] / 255, G.color[2] / 255);
      gl.uniform1f(loc.aa, 0.5 * W / px); gl.uniform1f(loc.range, G.range);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    // damped spring, fixed sub-step so behaviour is reproducible; snaps to the exact rest pose
    const K = 190, Cd = 22, KL = 420, CL = 30;
    // one fixed 1/240 s step of both springs; shared by the rAF loop and the deterministic test hook
    const h = 1 / 240;
    const integrate = () => {
      S.v += (-K * (S.t - S.target) - Cd * S.v) * h; S.t += S.v * h;
      S.leanV += (-KL * (S.lean - S.leanTarget) - CL * S.leanV) * h; S.lean += S.leanV * h;
    };
    const atRest = (live) => Math.abs(S.t - S.target) < 1e-4 && Math.abs(S.v) < 1e-3 && Math.abs(S.lean - S.leanTarget) < 1e-4 && Math.abs(S.leanV) < 1e-3 && !live;
    const snap = () => { S.t = S.target; S.v = 0; S.lean = S.leanTarget; S.leanV = 0; S.breath = 0; };
    function frame(now) {
      S.id = 0;
      if (!S.running) return; // setT() may have cancelled this scheduled spring.
      const dt = Math.min(0.05, (now - S.last) / 1000 || 0.016); S.last = now;
      for (let i = 0, n = Math.max(1, Math.round(dt / h)); i < n; i++) integrate();
      const live = S.breathUntil > now || S.ambient;
      if (live) { const ph = (now / 1000) * 2 * Math.PI / 2.4; const env = S.ambient ? 1 : Math.min(1, (S.breathUntil - now) / 600, (now - S.breathStart) / 400); S.breath = 0.012 * Math.sin(ph) * Math.max(0, env); } else S.breath = 0;
      const still = atRest(live);
      if (still) snap();
      render();
      if (still) { S.running = false; host.dispatchEvent(new CustomEvent("g6rig:rest", { detail: { id: mod3(Math.round(S.t)) } })); return; }
      S.id = requestAnimationFrame(frame);
    }
    const kick = () => { if (!S.running) { S.running = true; S.last = performance.now(); S.id = requestAnimationFrame(frame); } };
    const api = {
      get t() { return S.t; }, get id() { return mod3(Math.round(S.target)); }, get state() { return { ...S }; },
      setT(t) { if (S.id) cancelAnimationFrame(S.id); S.id = 0; S.running = false; S.t = S.target = t; S.v = 0; S.lean = S.leanTarget = 0; S.leanV = 0; S.breath = 0; render(); },
      goTo(id) {                                                                       // nearest equivalent pose to the current t: never more than 120deg
        const n = id + 3 * Math.round((S.t - id) / 3);
        if (reduced()) return api.setT(n);
        S.target = n; kick();
      },
      step(d = 1) { const n = Math.round(S.target) + d; if (reduced()) return api.setT(n); S.target = n; kick(); },
      hover(on) { if (reduced()) return; S.leanTarget = on ? 0.025 : 0; kick(); },
      press(on) { if (reduced()) return; S.leanTarget = on ? -0.025 : 0.0; kick(); },
      breathe(cycles = 3) { if (reduced()) return; S.breathStart = performance.now(); S.breathUntil = S.breathStart + cycles * 2400 + 600; kick(); },
      ambient(on) { if (reduced()) { S.ambient = false; return; } S.ambient = !!on; S.breathStart = performance.now(); kick(); },
      // deterministic stepping for tests: advances the springs by `sec` seconds without rAF; returns per-step extremes
      advance(sec, { draw = false } = {}) {
        let maxDt = 0, maxDv = 0, steps = Math.round(sec / h);
        for (let i = 0; i < steps; i++) { const t0 = S.t, v0 = S.v; integrate(); maxDt = Math.max(maxDt, Math.abs(S.t - t0)); maxDv = Math.max(maxDv, Math.abs(S.v - v0)); if (atRest(false)) { snap(); break; } }
        if (draw) render(); return { maxDt, maxDv };
      },
      render, el: host,
    };
    new ResizeObserver(() => render()).observe(host);
    document.addEventListener("visibilitychange", () => { if (!document.hidden && S.running) S.last = performance.now(); });
    render();
    return api;
  }
  window.G6Rig = { create };
})();
