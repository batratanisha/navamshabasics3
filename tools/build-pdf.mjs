// Render Navamsha-notes.html to Navamsha-notes.pdf. Requires playwright.
import { chromium } from 'playwright';
const root = new URL('..', import.meta.url).pathname;
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1200, height: 1600 } });
await p.goto('file://' + root + 'Navamsha-notes.html', { waitUntil: 'load' });
await p.evaluate(() => {
  document.documentElement.setAttribute('data-theme', 'light');
  document.querySelectorAll('.rev').forEach(e => e.classList.add('in'));
});
await p.emulateMedia({ media: 'print' });
await p.waitForTimeout(1200);
await p.pdf({
  path: root + 'Navamsha-notes.pdf', format: 'A4', printBackground: true,
  margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' },
  displayHeaderFooter: true,
  headerTemplate: '<div></div>',
  footerTemplate: '<div style="width:100%;font-size:8px;color:#8B7499;font-family:Georgia,serif;padding:0 12mm;display:flex;justify-content:space-between"><span style="font-style:italic">Karakamsha &amp; the Khara Pada</span><span class="pageNumber"></span></div>'
});
await b.close();
console.log('pdf written');
