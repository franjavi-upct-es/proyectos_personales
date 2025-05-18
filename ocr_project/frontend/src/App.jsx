import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';
import ScheduleForm from './components/ScheduleForm';
import ThemeOption from './components/ThemeOption';

export default function App() {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(theme === 'light' ? 'dark' : 'light');

  useEffect(() => {
    document.documentElement.className = theme;
  }, [theme]);

  return (
    <div className="p-4 max-w-lg mx-auto">
      <div
        style={{ position: 'fixed', top: '1rem', right: '1rem', cursor: 'pointer' }}
        onClick={toggleTheme}
      >
        <ThemeOption theme={theme} />
      </div>
      <h1 className="text-2xl font-bold mb-4">OCR Albaranes</h1>
      <UploadForm />
      <hr className="my-6" />
      <ScheduleForm />
    </div>
  );
}