function enviarPDFs() {
    const input = document.getElementById('pdfs');
    if (!input.files.length) {
        alert('Selecciona al menos un PDF.');
        return;
    }
    const data = new FormData();
    for (const file of input.files) {
        data.append('pdfs', file);
    }
    fetch('/procesar/', { method: 'POST', body: data })
        .then(res => res.json())
        .then(json => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';
            json.data.forEach((num, i) => {
                const line = document.createElement('p');
                line.textContent = `${input.files[i].name}: ${num || 'No detectado'}`;
                resultDiv.appendChild(line);
            });
        });
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}

document.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
});
