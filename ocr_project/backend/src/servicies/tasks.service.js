const fs = require('fs');
const path = require('path');
const { saveAlbaran, extractTextFromPdf, extractInfo, createAndMoveFile } = require('./ocr.service');

async function runFolder() {
    const folder = process.env.OCR_FOLDER;
    if (!folder || !fs.existsSync(folder)) return;
    for (const f of fs.readdirSync(folder)) {
        if (f.toLowerCase().endsWith('.pdf')) {
            const fullPath = path.join(folder, f);
            const text = await extractTextFromPdf(fullPath);
            const numero = extractInfo(text);
            createAndMoveFile(fullPath, numero, folder);
            await saveAlbaran(f, numero);
        }
    }
}

module.exports = { runFolder };