// Stacked telemetry traces, front to back, with one anomaly.
Lab.register({
  id: 'signals',
  name: 'Signals',
  tagline: 'All we ever see of production',
  concept: 'Nobody sees production directly; we see its signals. Hundreds of traces run across the book like the rows of an old pulsar plot: quiet at the edges, busy in the middle where the traffic is. Each line hides the ones behind it, as recent data hides history. On one row, in colour, something has started to happen.',
  plate: 'top',
  render(ctx) {
    const { W, H, rng, noise, pal } = ctx;
    const gap = rng.pick([18, 20, 22]), step = 6;
    const rows = Math.floor((H + 140) / gap);
    const hot = rng.int(Math.floor(rows * 0.45), Math.floor(rows * 0.8));
    const spikeX = ctx.front.x + ctx.front.w * rng.range(0.25, 0.75);
    let out = '';
    for (let r = 0; r < rows; r++) {
      const base = -60 + r * gap + gap;
      const pts = [];
      for (let x = -10; x <= W + 10; x += step) {
        const u = (x / W) * 2 - 1, env = Math.max(0, 1 - Math.pow(Math.abs(u) * 1.15, 2)) ** 1.6;
        let a = Math.max(0, noise.fbm(x / 70, r * 0.37, 3) + 0.15) * 70 * env + Math.abs(noise.fbm(x / 9, r * 1.7, 2)) * 6 * (0.3 + env);
        if (r === hot) a += 150 * Math.exp(-Math.pow((x - spikeX) / 26, 2)) + 55 * Math.exp(-Math.pow((x - spikeX - 70) / 40, 2));
        pts.push([x, base - a]);
      }
      const d = ctx.smooth(pts, false);
      out += `<path d="${d}L${W + 10} ${H + 20}L-10 ${H + 20}Z" fill="${pal.ground}"/>` + ctx.cased([{ d, color: r === hot ? ctx.accent(0) : null }]);
    }
    return out;
  },
});
