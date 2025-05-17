import { stat } from "fs";
import { useEffect, useState } from "react";

export default function ScheduleForm() {
    const [cron, setCron] = useState({hour: 0, minute: 0, second: 0});
    const [status, setStatus] = useState(null);

    useEffect(() => {
        fetch('http://localhost:4000/api/status')
            .then(r => r.json()).then(setStatus);
    }, []);

    const onSubmit = async e => {
        e.preventDefault();
        await fetch('http://localhost:4000/api/schedule', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ cron })
        });
        alert('Programación guardada');
        const s = await (await fetch('http://localhost:4000/api/status')).json();
        setStatus(s)
    };

    return (
        <div>
            <h2 className="text-xl font-semibold">Configurar Tarea</h2>
            <form onSubmit={onSubmit} className="space-y-2">
                {['hour', 'minute', 'second'].map(field => (
                <div key={field}>
                    <label>{field}: </label>
                    <input 
                        type="number"
                        min="0" max={field === 'hour'?23:59}
                        value={cron[field]}
                        onChange={e => setCron({...cron, [field]: +e.target.value})}
                    />
                </div>
                ))}
            </form>
            <p className="mt-2">
                {status
                    ? status.scheduled
                        ? `Próxima ejecución: ${new Date(status.nextRun).toLocaleString()}`
                        : 'Tarea no programada'
                    : "Cargando estado..."}
            </p>
        </div>
    );
}