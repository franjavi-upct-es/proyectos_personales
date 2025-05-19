require('dotenv').config();
const express = require('express');
const cors = require('cors');
const albaranesRoutes = require('./routes/albaranes.routes');
const oracledb = require('oracledb');

const app = express();
app.use(cors());
app.use(express.json());

// Configuración de la conexión a la base de datos Oracle
oracledb.createPool({
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  connectString: process.env.DB_CONNECT_STRING
}, (err, pool) => {
  if (err) {
    console.error('Error al crear el pool de conexiones:', err);
    return;
  }
  console.log('Pool de conexiones a la base de datos Oracle creado');
});

app.use('/api', albaranesRoutes);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
