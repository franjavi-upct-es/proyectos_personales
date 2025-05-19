const { Schema } = require('mongoose');

const AlbaranSchema = new Schema({
    archivo:    { type: String, required: true },
    numero:     { type: String },
    fecha:      { type: String },
    proveedor:  { type: String },
    total:      { type: Number },
    creado_en:  { type: Date, default: () => new Date() }
});

// module.exports = model('Albaran', AlbaranSchema)