import React, { useState } from 'react';

export default function UploadForm() {
  const [file, setFile] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    if (!file) return;

    const form = new FormData();
    form.append('pdf', file);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
        method: 'POST',
        body: form,
      });
      // ... manejar respuesta
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="application/pdf"
        onChange={e => setFile(e.target.files[0])}
      />
      <button type="submit">Subir PDF</button>
    </form>
  );
}