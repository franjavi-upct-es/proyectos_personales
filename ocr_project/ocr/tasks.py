import os
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Albaran
from .ocr_albaranes import extract_text_from_pdf, extract_info, create_and_move_file

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
JOB_ID = 'ocr_job'

def run_folder():
    folder = os.getenv('OCR_FOLDER')
    if not folder or not os.path.isdir(folder):
        return
    for fname in os.listdir(folder):
        if fname.lower().endswith('.pdf'):
            path = os.path.join(folder, fname)
            text = extract_text_from_pdf(path)
            numero = extract_info(text)
            create_and_move_file(path, numero, folder)
            Albaran.objects.create(archivo=fname, numero=numero)

def reschedule_job(cron):
    try:
        scheduler.remove_job(JOB_ID)
    except Exception:
        pass
    scheduler.add_job(
        run_folder,
        trigger='cron',
        id=JOB_ID,
        hour=cron.get('hour', 0),
        minute=cron.get('minute', 0),
        second=cron.get('second', 0)
    )

def get_next_run():
    job = scheduler.get_job(JOB_ID)
    return job.next_run_time if job else None

def start():
    if not scheduler.running:
        scheduler.start()
