const fileInput = document.getElementById('fileInput');
const processBtn = document.getElementById('processBtn');
const configBtn = document.getElementById('configScheduleBtn');
const log = document.getElementById('log');

processBtn.addEventListener('click', async () => {
    const files = fileInput.files;
    if (!files.length) {
        alert('Selecciona una carpeta.');
        return;
    }

    const form = new FormData();
    for (let f of files) {
        // Incluye ruta relativa para distringuir entre archivos
        form.append('pdfs', f, f.webkitRelativePath);
    }

    log.textContent = 'Procesando...';
    try {
        const res = await fetch('/process', { method: 'POST', body: form });
        const json = await res.json();
        if (json.status === 'success') {
            log.textContent += 'OK:\n' + JSON.stringify(json.data, null, 2); 
        } else {
            log.textContent += 'Error: ' + json.message;
        }
    } catch (error) {
        log.textContent += 'Error de red: ' + error.message;
    }
});

configBtn.addEventListener('click', () => {
    window.location = '/schedule-config';
})