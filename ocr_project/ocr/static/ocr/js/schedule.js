document.getElementById('configForm').addEventListener('submit', e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    for (let k in data) data[k] = parseInt(data[k], 10);
    fetch('/api/schedule/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cron: data })
    }).then(() => location.reload());
});

fetch('/api/status/')
    .then(res => res.json())
    .then(data => {
        const status = document.getElementById('status');
        status.innerText = data.scheduled
            ? `Próxima ejecución: ${data.next_run}`
            : 'Tarea no programada';
    });

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
