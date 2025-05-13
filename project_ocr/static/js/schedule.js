const form = document.getElementById('scheduleForm');
const statusDiv = document.getElementById('status');

// Consultar estado actual al cargar
fetch('/schedule-status')
  .then(r => r.json())
  .then(json => {
    statusDiv.textContent = json.scheduled
      ? 'Próxima ejecución: ' + new Date(json.next_run).toLocaleString()
      : 'No hay tarea programada';
  });

form.addEventListener('submit', async ev => {
  ev.preventDefault();
  const hour = parseInt(document.getElementById('hour').value, 10);
  const minute = parseInt(document.getElementById('minute').value, 10);
  const res = await fetch('/schedule', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ cron: { hour, minute } })
  });
  const json = await res.json();
  if (json.status === 'success') {
    statusDiv.textContent =
      'Horario guardado. Se ejecutará cada día a ' +
      String(hour).padStart(2, '0') + ':' + String(minute).padStart(2, '0');
  }
});
