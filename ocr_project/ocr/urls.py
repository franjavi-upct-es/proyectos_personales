from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('configurar/', views.schedule_config, name='schedule_config'),
    path('procesar/', views.process_pdfs, name='process_pdfs'),
    path('exportar/', views.export_excel, name='export_excel'),
    path('api/schedule/', views.schedule_job, name='schedule_job'),
    path('api/status/', views.schedule_status, name='schedule_status'),
]
