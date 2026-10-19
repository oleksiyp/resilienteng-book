// Contour terrain with one trajectory drifting toward the boundary.
Lab.register({
  id: 'drift',
  name: 'Drift',
  tagline: 'Toward the boundary, one reasonable step at a time',
  concept: 'Jens Rasmussen drew safety as a landscape: pressures for efficiency and less effort push every operation, step by step, toward a boundary nobody can see. Here the terrain is a contour map, and one path wanders across the whole book, each step locally sensible, climbing toward the line where things fail. Running production is the craft of noticing the drift.',
  plate: 'top',
  render(ctx) {
    const { W, H, rng, noise } = ctx;
    const sc = rng.range(1 / 800, 1 / 480), warp = rng.range(0.8, 1.8), cs = 6;
    const gw = Math.ceil(W / cs) + 3, gh = Math.ceil(H / cs) + 3;
    const f = new Float32Array(gw * gh);
    let lo = Infinity, hi = -Infinity;
    for (let j = 0; j < gh; j++) for (let i = 0; i < gw; i++) {
      const x = (i - 1) * cs * sc, y = (j - 1) * cs * sc;
      const qx = noise.fbm(x + 3.1, y + 7.7, 3), qy = noise.fbm(x - 5.2, y + 1.3, 3);
      const v = noise.fbm(x + warp * qx, y + warp * qy, 4) + 0.6 * (i / gw);
      f[j * gw + i] = v; lo = Math.min(lo, v); hi = Math.max(hi, v);
    }
    const at = (x, y) => { const i = Math.max(0, Math.min(gw - 2, x / cs + 1)), j = Math.max(0, Math.min(gh - 2, y / cs + 1)); const i0 = i | 0, j0 = j | 0, a = i - i0, b = j - j0; const k = j0 * gw + i0; return f[k] * (1 - a) * (1 - b) + f[k + 1] * a * (1 - b) + f[k + gw] * (1 - a) * b + f[k + gw + 1] * a * b; };
    const n = rng.int(14, 20);
    // the boundary: the contour through a point low on the front cover, where the path will arrive
    const tx0 = ctx.front.x + ctx.front.w * rng.range(0.55, 0.8), ty0 = ctx.front.y + ctx.front.h * rng.range(0.6, 0.8);
    const boundary = at(tx0, ty0);
    const strokes = [];
    const levels = [];
    for (let k = 1; k < n; k++) levels.push(lo + (hi - lo) * k / n);
    for (const level of levels) {
      if (Math.abs(level - boundary) < (hi - lo) / n * 0.5) continue;
      for (const c of ctx.contours(f, gw, gh, cs, level, -cs, -cs)) {
        for (const r of ctx.runs(c.pts.filter((_, i) => i % 2 === 0), (x, y) => ctx.free(x, y, 2))) {
          if (!r.v || r.pts.length < 3) continue;
          const closed = c.closed && r.pts.length === Math.ceil(c.pts.length / 2);
          strokes.push({ d: ctx.smooth(r.pts, closed), color: null });
        }
      }
    }
    {
      const comps = ctx.contours(f, gw, gh, cs, boundary, -cs, -cs);
      const dist = c => Math.min(...c.pts.map(p => Math.hypot(p[0] - tx0, p[1] - ty0)));
      const c = comps.reduce((a, b) => (dist(b) < dist(a) ? b : a));
      for (const r of ctx.runs(c.pts.filter((_, i) => i % 2 === 0), (x, y) => ctx.free(x, y, 2))) {
        if (!r.v || r.pts.length < 3) continue;
        strokes.push({ d: ctx.smooth(r.pts, false), color: ctx.accent(1) });
      }
    }
    // the path: each step mostly along the local contour (no change in risk), with a slow pull toward the boundary point
    const pts = [];
    let x = ctx.back.x + ctx.back.w * rng.range(0.1, 0.25), y = ctx.back.y + ctx.back.h * rng.range(0.6, 0.8), heading = 0;
    const flush = () => { if (pts.length > 2) strokes.push({ d: ctx.smooth(pts.splice(0), false), color: ctx.accent(0) }); else pts.length = 0; };
    for (let s = 0; s < 6000; s++) {
      const e = 3, gx = (at(x + e, y) - at(x - e, y)) / (2 * e), gy = (at(x, y + e) - at(x, y - e)) / (2 * e), gl = Math.hypot(gx, gy) || 1e-9;
      const ax = tx0 - x, ay = ty0 - y, al = Math.hypot(ax, ay);
      if (al < 30) break;
      let cx = -gy / gl, cy = gx / gl;
      if (cx * ax + cy * ay < 0) { cx = -cx; cy = -cy; }
      const pull = 0.35 + 0.25 * noise.fbm(s / 120, 4.2, 2);
      const want = Math.atan2(cy * (1 - pull) + (ay / al) * pull, cx * (1 - pull) + (ax / al) * pull) + 0.5 * noise.fbm(s / 70, 1.7, 2);
      let dh = Math.atan2(Math.sin(want - heading), Math.cos(want - heading));
      heading += Math.max(-0.12, Math.min(0.12, dh));
      x += 4 * Math.cos(heading); y += 4 * Math.sin(heading);
      if (ctx.free(x, y, 6)) pts.push([x, y]); else flush();
    }
    pts.push([tx0, ty0]); flush();
    strokes.push({ d: `M${tx0.toFixed(1)} ${ty0.toFixed(1)}m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0`, color: ctx.accent(0), w: ctx.lw * 3 });
    return ctx.cased(strokes);
  },
});
