import { useEffect, useState } from 'react';

export default function ScheduleForm() {
  const [cron, setCron] = useState({ hour: 0, minute: 0 });
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetch('http://localhost:4000/api/status')
      .then(r => r.json())
      .then(setStatus);
  }, []);

  const onSubmit = async e => {
    e.preventDefault();
    await fetch('http://localhost:4000/api/schedule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cron })
    });
    alert('Programación guardada');
    const s = await (await fetch('http://localhost:4000/api/status')).json();
    setStatus(s);
  };

return (
    <div>
        <h2 className="text-xl font-semibold">Configurar Tarea</h2>
        <form onSubmit={onSubmit} className="space-y-2">
            <div className="flex flex-row items-center space-x-4 justify-center">
                <div className="flex flex-col items-center">
                    <label htmlFor="hour" className="text-xs">Hora</label>
                    <input
                        id="hour"
                        type="number"
                        min="0"
                        max="23"
                        value={cron.hour}
                        onChange={e => setCron({ ...cron, hour: +e.target.value })}
                        className="w-16 text-center"
                    />
                </div>
                <div className="flex flex-col items-center">
                    <label htmlFor="minute" className="text-xs">Minuto</label>
                    <input
                        id="minute"
                        type="number"
                        min="0"
                        max="59"
                        value={cron.minute}
                        onChange={e => setCron({ ...cron, minute: +e.target.value })}
                        className="w-16 text-center"
                    />
                </div>
            </div>
            <button type="submit" className="btn">Guardar</button>
        </form>
        <p className="mt-2">
            {status
                ? status.scheduled
                    ? `Próxima ejecución: ${new Date(status.nextRun).toLocaleString()}`
                    : 'Tarea no programada'
                : 'Cargando estado...'}
        </p>
    </div>
);
}