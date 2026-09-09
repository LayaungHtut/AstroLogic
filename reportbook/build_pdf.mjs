// Split PDF rendering for the AstroLogic report.
//   node build_pdf.mjs body <outPath>   -> body sections only, page-numbered footer starting at 1
//   node build_pdf.mjs front <outPath>  -> cover + group/roles/contents only, no footer (unnumbered)
//
// Full rebuild workflow (from reportbook/), after editing report.html:
//   1. node build_pdf.mjs body pass1.pdf
//   2. Extract each "sec-*" heading's page number from pass1.pdf (e.g. with pypdf)
//      and update the <span class="toc-page" data-target="...">N</span> values
//      in report.html's Contents list.
//   3. node build_pdf.mjs front front.pdf
//   4. node build_pdf.mjs body body.pdf
//   5. Merge front.pdf + body.pdf (e.g. with pypdf's PdfWriter) into AstroLogic_Report.pdf.
import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const reportPath = path.join(__dirname, 'report.html');
const fileUrl = 'file:///' + reportPath.replace(/\\/g, '/');

const footerTemplate = `
  <div style="width:100%; font-size:9px; font-family:'Times New Roman',serif; color:#555; text-align:center;">
    <span class="pageNumber"></span>
  </div>`;
const emptyTemplate = `<div></div>`;

async function renderBodyOnly(browser, outPath) {
	const page = await browser.newPage();
	await page.goto(fileUrl, { waitUntil: 'networkidle' });
	await page.evaluate(() => document.body.classList.add('print-body-only'));
	// In this isolated pass, "Introduction" becomes the literal first page of
	// the PDF, so the report's `@page :first { margin: 0 }` rule (meant only
	// for the real cover page) would otherwise wrongly zero out its margins.
	await page.addStyleTag({
		content: '@page :first { margin: 25mm 22mm 22mm 22mm !important; }'
	});
	await page.pdf({
		path: outPath,
		format: 'A4',
		printBackground: true,
		preferCSSPageSize: true,
		displayHeaderFooter: true,
		headerTemplate: emptyTemplate,
		footerTemplate,
		margin: { top: '25mm', bottom: '22mm', left: '22mm', right: '22mm' }
	});
	await page.close();
}

async function renderFrontOnly(browser, outPath) {
	const page = await browser.newPage();
	await page.goto(fileUrl, { waitUntil: 'networkidle' });
	await page.evaluate(() => document.body.classList.add('print-front-only'));
	await page.pdf({
		path: outPath,
		format: 'A4',
		printBackground: true,
		preferCSSPageSize: true,
		displayHeaderFooter: false,
		margin: { top: '0mm', bottom: '0mm', left: '0mm', right: '0mm' }
	});
	await page.close();
}

const mode = process.argv[2];
const outPath = process.argv[3];

const browser = await chromium.launch();
if (mode === 'body') {
	await renderBodyOnly(browser, outPath);
} else if (mode === 'front') {
	await renderFrontOnly(browser, outPath);
} else {
	console.error('usage: node build_pdf.mjs <body|front> <outPath>');
	process.exit(1);
}
await browser.close();
console.log('wrote', outPath);
