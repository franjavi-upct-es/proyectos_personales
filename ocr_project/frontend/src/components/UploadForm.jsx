import { useState } from 'react';

export default function UploadForm() {
  const [results, setResults] = useState([]);

  const onSubmit = async e => {
    e.preventDefault();
    const files = e.target.pdfs.files;
    if (!files.length) return alert('Selecciona al menos un PDF.');
    const data = new FormData();
    Array.from(files).forEach(f => data.append('pdfs', f));
    const res = await fetch('http://localhost:4000/api/procesar', {
      method: 'POST', body: data
    });
    const json = await res.json();
    setResults(json.data);
  };

  return (
    <form onSubmit={onSubmit} className="space-y-2">
      <input type="file" name="pdfs" multiple />
      <button type="submit" className="btn">Procesar</button>
      <div>
        {results.map((num, i) => (
          <p key={i}>Archivo {i+1}: {num || 'No detectado'}</p>
        ))}
      </div>
    </form>
  );
}
