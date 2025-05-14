from django.core.management.base import BaseCommand
from ocr.tasks import run_folder

class Command(BaseCommand):
    help = 'Escanea la carpeta OCR_FOLDER y procesa todos los PDFs.'

    def handle(self, *args, **options):
        run_folder()
        self.stdout.write(self.style.SUCCESS('OCR completado manualmente.'))
