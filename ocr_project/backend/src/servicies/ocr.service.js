const { convert } = require('pdf-poppler');
const { createWorker } = require('tesseract.js');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const oracledb = require('oracledb');

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

// Ejecuta el script Python para procesar una carpeta de PDFs
function processAlbaranesFolder(folderPath) {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../ocr_albaranes.py');
        const py = spawn('python', [scriptPath, folderPath]);
        let output = '';
        let error = '';
        py.stdout.on('data', (data) => { output += data.toString(); });
        py.stderr.on('data', (data) => { error += data.toString(); });
        py.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                reject(error || output);
            }
        });
    });
}

const ORACLE_USER = process.env.ORACLE_USER || 'usuario';
const ORACLE_PASSWORD = process.env.ORACLE_PASSWORD || 'password';
const ORACLE_CONNECT_STRING = process.env.ORACLE_CONNECT_STRING || 'localhost:1521/ORCLPDB1';

async function saveAlbaran(archivo, numero) {
    let connection;
    try {
        connection = await oracledb.getConnection({
            user: ORACLE_USER,
            password: ORACLE_PASSWORD,
            connectString: ORACLE_CONNECT_STRING
        });
        await connection.execute(
            `INSERT INTO ALBARANES (ARCHIVO, NUMERO) VALUES (:archivo, :numero)`,
            { archivo, numero },
            { autoCommit: true }
        );
    } finally {
        if (connection) await connection.close();
    }
}

module.exports = { extractTextFromPdf, extractInfo, createAndMoveFile, processAlbaranesFolder, saveAlbaran };