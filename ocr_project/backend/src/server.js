require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const albaranesRoutes = require('./routes/alabaranes.routes');
const { use } = require('react');

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true, useUnifiedTopology: true
})
.then(() => console.log('MongoDB conectado')) 
.catch(err => console.log(err));

app.use('/api', albaranesRoutes);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
