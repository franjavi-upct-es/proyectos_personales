const { convert } = require('pdf-poppler');
const { createWorker } = require('tesseract.js');
const path = require('path');
const fs = require('fs');

const worker = createWorker({
    langPath: process.env.TESSDATA_PREFIX,
    gzip: false
});

async function extractTextFromPdf(pdfPath) {
    const outputDir = path.dirname(pdfPath);
    await convert(pdfPath, {
        format: 'png',
        out_dir: outputDir,
        out_prefix: path.basename(pdfPath, '.pdf'),
        dpi: 300
    });
    const images = fs.readdirSync(outputDir)
        .filter(f => f.startsWith(path.basename(pdfPath, '.pdf')) && f.endsWith('png'))
        .map(f => path.join(outputDir, f));

    await worker.load();
    await worker.loadLanguage('spa');
    await worker.initialize('spa');

    let fullText = '';
    for (const img of images) {
        const { data: { text } } = await worker.recognize(img, {
            tessjs_create_tsv: '0',
            tessjs_create_hocr: '0',
            psm: 6
        });
        fullText += text;
        fs.unlinkSync(img);
    }
    await worker.terminate();
    return fullText;
}

function extractInfo(text) {
    const year = new Date().getFullYear() % 100;
    const regex = new RegExp(`\\b(?:[A-Z]{${year}}\\d{5}|AA${year}\\d{4})\\b`);
    const match = text.match(regex);
    return match ? match[0] : null;
}

function createAndMoveFile(pdfPath, numero, baseDir) {
    if (!numero) return;
    const year = new Date().getFullYear();
    const isAA = numero.startsWith('AA');
    const serie = isAA ? 'Serie AA' : `Serie ${numero[0]}`;
    const folderName = isAA
        ? `${year} ${numero.slice(0, 4)}`
        : `${year} ${numero.slice(0, 3)}`;

    const targetDir = path.join(baseDir, `ALBARANES ${serie}`, folderName);
    fs.mkdirSync(targetDir, { recursive: true });
    const newPath = path.join(targetDir, `${numero}.pdf`);
    if (!fs.existsSync(newPath)) fs.renameSync(pdfPath, newPath);
}

module.exports = { extractTextFromPdf, extractInfo, createAndMoveFile };