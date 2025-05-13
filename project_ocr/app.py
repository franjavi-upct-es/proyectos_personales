from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import os, tempfile, atexit
import ocr_albaranes

app = Flask(__name__)

# Configuración del scheduler en segundo plano
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Referencia al job programado
job = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule-config')
def scheduler_config():
    return render_template('schedule.html')

@app.route('/process', methods=['POST'])
def process():
    files = request.files.getlist('pdfs')
    if not files:
        return jsonify({'status': 'error', 'message': 'No se han enviado archivos'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        info = []
        for f in files:
            path = os.path.join(tmpdir, f.filename)
            f.save(path)
            text = ocr_albaranes.extract_text_from_pdf(path)
            info.append(ocr_albaranes.extract_info(text))
        return jsonify({'status': 'success', 'data': info})

@app.route('/schedule', methods=['POST'])
def schedule_job():
    global job
    data = request.json
    if job:
        scheduler.remove_job('ocr_job')
    # Creamos el nuevo job diario
    job = scheduler.add_job(
        func=run_folder,
        trigger='cron',
        id='ocr_job',
        **data['cron']
    )
    return jsonify({'status': 'success'})

@app.route('/schedule-status')
def schedule_status():
    if job:
        return jsonify({
            'scheduled': True,
            'next_run': job.next_run_time.isoformat()
        })
    return jsonify({'schedule': False})

def run_folder():
    """
    Función que recorre la carpeta definida en OCR_FOLDER,
    procesa todos los PDFs y mueve/guarda los resultados.
    """
    folder = os.getenv('OCR_FOLDER')
    if not folder or not os.path.isdir(folder):
        app.logger.error('OCR_FOLDER no configurada o inválida')
        return

    for fname in os.listdir(folder):
        if fname.lower().endswith('.pdf'):
            path = os.path.join(folder, fname)
            text = ocr_albaranes.extract_text_from_pdf(path)
            info = ocr_albaranes.extract_info(text)
            ocr_albaranes.create_and_move_file(info, folder)
    app.logger.info('Automatización OCR completada')

if __name__ == '__main__':
    app.run(debug=True)
