// Renders a screenshot of index.html with each colour scheme from
// schemes.json applied, for embedding in design-options.pdf.
// Usage: node render_scheme_previews.js <output-dir>
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const outDir = process.argv[2] || 'previews';
fs.mkdirSync(outDir, { recursive: true });
const schemes = JSON.parse(fs.readFileSync(path.join(__dirname, 'schemes.json'), 'utf8'));
const sitePath = 'file://' + path.resolve(__dirname, '..', 'index.html');

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium',
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 1180 } });
  await page.goto(sitePath);
  for (let i = 0; i < schemes.length; i++) {
    const [name, , primary, dark, accent, light, ink] = schemes[i];
    await page.addStyleTag({
      content: `:root{--primary:${primary};--dark:${dark};--accent:${accent};--light:${light};--ink:${ink};}`,
    });
    await page.screenshot({
      path: path.join(outDir, `scheme-${String(i + 1).padStart(2, '0')}.png`),
      clip: { x: 0, y: 0, width: 1280, height: 1180 },
    });
    console.log(`rendered ${i + 1}/${schemes.length} ${name}`);
  }
  await browser.close();
})();
