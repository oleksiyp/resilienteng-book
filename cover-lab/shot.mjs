import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const p = await b.newPage(); await p.setViewport({ width: 1900, height: 500 });
await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle0' }); await p.screenshot({ path: process.argv[3], fullPage: true }); await b.close();
