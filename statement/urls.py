from .views import PDFFileCreateView,TestView,StatementView,BankView,TransactionView,BankStatementUploadView
from django.urls import path
urlpatterns = [
    path('pdf-files/', PDFFileCreateView.as_view(), name='pdf_file_create'),
    path('banks/', BankView.as_view(), name='bank'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('statementUpload/', BankStatementUploadView.as_view(), name='upload'),
    path('statements/<pk>', StatementView.as_view()),
    path('', TestView.as_view(), name='test')
]