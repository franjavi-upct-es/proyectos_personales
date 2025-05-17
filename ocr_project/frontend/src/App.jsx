import UploadForm from './components/UploadForm';
import ScheduleForm from './components/ScheduleForm';

export default function App() {
  return (
    <div className='p-4 max-w-lg mx-auto'>
      <h1 className='text-2xl font-bold mb-4'>OCR Albaranes</h1>
      <UploadForm />
      <hr className='my-6'/>
      <ScheduleForm />
    </div>
  )
}
