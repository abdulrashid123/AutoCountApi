from .views import PDFFileCreateView,TestView
from django.urls import path
urlpatterns = [
    path('pdf-files/', PDFFileCreateView.as_view(), name='pdf_file_create'),
    path('', TestView.as_view(), name='test')
]