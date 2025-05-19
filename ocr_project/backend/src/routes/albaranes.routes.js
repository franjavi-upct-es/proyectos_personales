const router = require('express').Router();
const ctrl = require('../controllers/albaranes.controller');

router.post('/procesar', ctrl.processPdfs);
router.post('/schedule', ctrl.schedule);
router.get('/status', ctrl.status);
router.post('/procesar-carpeta', ctrl.processFolder);

module.exports = router;