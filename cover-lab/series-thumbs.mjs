// Renders small front and spine thumbnails of every book in the series for the shelf
// on the title page: node cover-lab/series-thumbs.mjs  → assets/series/<key>-{front,spine}.png
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, '../assets/series');
const BOOKS = {
  architecture: { svg: '../../arch-site/assets/cover/wrap.svg', spineW: 55 },
  resilience:   { svg: '../assets/cover/wrap.svg', spineW: 75 },
  operations:   { svg: '../../prod-systems/assets/cover/wrap.svg', spineW: 70 },
};
const FRONT_PX = 360;   // 2x of the ~180 px shown on desktop

const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage();
for (const [key, b] of Object.entries(BOOKS)) {
  const svg = fs.readFileSync(path.join(here, b.svg), 'utf8');
  const W = 12.5 + 600 + b.spineW + 600 + 12.5;
  const scale = FRONT_PX / 600;
  const H = Math.round(900 * scale);
  const shots = { spine: { x: 612.5, w: b.spineW }, front: { x: 612.5 + b.spineW, w: 600 } };
  for (const [part, r] of Object.entries(shots)) {
    const w = Math.round(r.w * scale);
    await page.setViewport({ width: w, height: H });
    await page.setContent(`<html><body style="margin:0;overflow:hidden">
      <div style="width:${w}px;height:${H}px;overflow:hidden;position:relative">
      <div style="position:absolute;left:${-r.x * scale}px;top:${-12.5 * scale}px;width:${W * scale}px;height:${925 * scale}px">
      ${svg.replace(/<\?xml[^>]*>/, '').replace('<svg ', `<svg width="${W * scale}" height="${925 * scale}" `)}
      </div></div></body></html>`);
    await page.screenshot({ path: path.join(out, `${key}-${part}.png`), clip: { x: 0, y: 0, width: w, height: H } });
  }
}
await browser.close();
console.log('thumbs done');
