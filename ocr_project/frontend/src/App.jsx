import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';
import ScheduleForm from './components/ScheduleForm';
import ThemeOption from './components/ThemeOption';

export default function App() {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(theme === 'light' ? 'dark' : 'light');

  useEffect(() => {
    document.documentElement.className = theme;
    document.body.style.backgroundColor = theme === 'dark' ? '#121212' : '#fff';
    document.body.style.color = theme === 'dark' ? '#eee' : '#000';
  }, [theme]);

  return (
    <div className="p-4 max-w-lg mx-auto">
      {/* Use a controlled checkbox for toggling */}
      <label className="toggle-switch">
        <input
          type="checkbox"
          checked={theme === 'dark'}
          onChange={toggleTheme}
        />
        <span className="slider"></span>
      </label>

      <h1 className="text-2xl font-bold mb-4">OCR Albaranes</h1>
      <UploadForm />
      <hr className="my-6" />
      <ScheduleForm />
    </div>
  );
}