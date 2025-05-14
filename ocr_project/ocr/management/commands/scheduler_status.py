from django.core.management.base import BaseCommand
from ocr.tasks import get_next_run

class Command(BaseCommand):
    help = 'Muestra la próxima ejecución programada del scheduler.'

    def handle(self, *args, **options):
        next_run = get_next_run()
        if next_run:
            self.stdout.write(f'Próxima ejecución: {next_run}')
        else:
            self.stdout.write('No hay tarea programada.')
