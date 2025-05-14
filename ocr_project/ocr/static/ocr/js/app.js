function enviarPDFs() {
    const input = document.getElementById('pdfs');
    const data = new FormData();
    for (const file of input.files) {
        data.append('pdfs', file);
    }
    fetch('/procesar/', {
        method: 'POST',
        body: data
    })
    .then(res => res.json())
    .then(res => {
        document.getElementById('result').innerText = JSON.stringify(res, null, 2);
    });
}
