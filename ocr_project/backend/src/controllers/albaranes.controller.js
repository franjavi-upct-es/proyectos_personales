const multer = require('multer');
const tmp = require('tmp');
const fs = require('fs');
const path = require('path');
const Albaran = require('../models/Alabaran.model');
const { extractTextFromPdf, extractInfo } = require('../servicies/ocr.service')
const { scheduleJob, getStatus } = require('../servicies/scheduler.service')

const upload = multer({ dest: tmp.dirSync().name });

exports.processPdfs = [
    upload.array('pdfs'),
    async (req, res) => {
        const resultados = [];
        for (const file of req.files) {
            const text = await extractTextFromPdf(file.path);
            const numero = extractInfo(text);
            await Albaran.create({ archivo: file.originalname, numero });
            resultados.push(numero);
            fs.unlinkSync(file.path);
        }
        res.json({ status: 'success', data: resultados });
    }
];

exports.schedule = (req, res) => {
    scheduleJob(req.body.cron || {});
    res.json({ status: 'sucess' });
};

exports.status = (req, res) => {
    res.json(getStatus());
};