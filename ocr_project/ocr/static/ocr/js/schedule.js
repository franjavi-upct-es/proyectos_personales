document.getElementById('configForm').addEventListener('submit', e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    for (let key in data) data[key] = parseInt(data[key]);
    fetch('/api/schedule/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cron: data })
    })
    .then(res => res.json())
    .then(() => location.reload());
});

fetch('/api/status/')
    .then(res => res.json())
    .then(data => {
        if (data.scheduled) {
            document.getElementById('status').innerText = 'Próxima ejecución: ' + data.next_run;
        } else {
            document.getElementById('status').innerText = 'Tarea no programada';
        }
    });
