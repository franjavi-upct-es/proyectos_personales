import os
import tempfile
import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Albaran
from .tasks import reschedule_job, get_next_run
from .ocr_albaranes import extract_text_from_pdf, extract_number

def index(request):
    return render(request, 'ocr/index.html')

def schedule_config(request):
    return render(request, 'ocr/schedule.html')

@csrf_exempt
@require_POST
def process_pdfs(request):
    files = request.FILES.getlist('pdfs')
    info = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for f in files:
            path = os.path.join(tmpdir, f.name)
            with open(path, 'wb') as dest:
                for chunck in f.chuncks(): dest.write(chunck)
            text = extract_text_from_pdf(path)
            numero = extract_number(text)
            Albaran.objetcs.create(archivo=f.name, numero=numero)
            info.append(numero)
    return JsonResponse({'status': 'success', 'data': info})

@csrf_exempt
@require_POST
def schedule_job(request):
    data = json.loads(request.body)
    reschedule_job(data.get('cron', {}))
    return JsonResponse({'status': 'success'})


def schedule_status(request):
    next_run = get_next_run()
    return JsonResponse({'scheduled': bool(next_run), 'next_run': next_run.isoformat() if next_run else None})


def export_excel(request):
    albaranes = Albaran.objects.all()
    df = pd.DataFrame([{
        'Archivo': a.archivo,
        'Número': a.numero,
        'Fecha': a.fecha,
        'Proveedor': a.proveedor,
        'Total': a.total,
        'Creado': a.creado_en
    } for a in albaranes])
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="albaranes.xlsx"'
        return response
