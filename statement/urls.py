from .views import PDFFileCreateView
from django.urls import path
urlpatterns = [
    path('pdf-files/', PDFFileCreateView.as_view(), name='pdf_file_create')
]