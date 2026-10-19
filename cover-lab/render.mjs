// Render candidate covers to PNG for review. Usage: (serve this folder on :8766) node render.mjs outdir design:seed[:k=v,...] ...
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
const [out, ...jobs] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const BASE = { palette: 'paper', accents: 'both', weight: '4/2', plateStyle: 'boxed', plate: 'auto', font: 'archivo', spine: 0.7 };
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage();
page.on('console', m => { if (m.type() === 'error') console.log('[page]', m.text()); });
await page.goto('http://localhost:8766/index.html', { waitUntil: 'networkidle0' });
for (const job of jobs) {
  const [design, seed, extra] = job.split(':');
  const cfg = { ...BASE, seed: +seed };
  if (extra) for (const kv of extra.split(',')) { const [k, v] = kv.split('='); cfg[k] = v.startsWith('[') ? JSON.parse(v) : (isNaN(+v) ? v : +v); }
  const r = await page.evaluate(async (design, cfg) => {
    const d = Lab.designs.find(x => x.id === design);
    const r = await Lab.build(d, cfg, true);
    return { svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${r.geo.W} ${r.geo.H}" width="${r.geo.W}" height="${r.geo.H}">${r.markup}</svg>`, geo: r.geo, ms: r.ms };
  }, design, cfg);
  const name = `${design}-${seed}${extra ? '-' + extra.replace(/[^a-z0-9]+/gi, '') : ''}`;
  writeFileSync(`${out}/${name}.svg`, r.svg);
  const p2 = await browser.newPage();
  await p2.setViewport({ width: r.geo.W, height: r.geo.H, deviceScaleFactor: 1 });
  await p2.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;900&family=IBM+Plex+Mono:wght@500&family=Source+Serif+4:ital,wght@0,400;0,700;1,400&display=block"></head><body style="margin:0">${r.svg}</body></html>`, { waitUntil: 'networkidle0' });
  await p2.evaluate(() => document.fonts.ready);
  await p2.screenshot({ path: `${out}/${name}-wrap.png` });
  await p2.screenshot({ path: `${out}/${name}-front.png`, clip: { x: r.geo.front.x - 12, y: 0, width: r.geo.front.w + 25, height: r.geo.H } });
  await p2.close();
  console.log('rendered', name, r.ms + 'ms');
}
await browser.close();
