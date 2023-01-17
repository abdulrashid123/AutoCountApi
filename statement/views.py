from rest_framework import generics
from .serializers import StatementUploadSerializer,StatementSerializer,BankSerializer,TransactionSerializer
from .models import StatementUpload,Statement,Bank,Transaction
from rest_framework.response import Response
from rest_framework import status
from statement.tasks import test,parseStatement
from rest_framework.views import APIView
from rest_framework import generics
class PDFFileCreateView(APIView):

    def post(self, request, *args, **kwargs):
        bank = request.data.pop('bank')
        serializer = StatementUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        id = serializer.data['id']
        obj = Bank.objects.get(name=bank[0])
        stat_obj = StatementUpload.objects.get(id=id)
        stat_obj.bank = obj
        stat_obj.save()
        parseStatement.delay(serializer.data['file'],bank,id)
        return Response("https://stackoverflow.com/questions/45398323/django-str-object-has-no-attribute-values-in-rest-framework", status=status.HTTP_201_CREATED)


class StatementView(APIView):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer

    def get(self,request,pk=None):
        data = Statement.objects.filter(statementUpload__id=pk)
        serializer = StatementSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class BankView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankStatementUploadView(generics.ListAPIView):
    queryset = StatementUpload.objects.all()
    serializer_class = StatementUploadSerializer

class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        statement_id = self.request.data[0].get("statement")
        obj = Statement.objects.get(id=statement_id)
        serializer.save(statement=obj)

class TestView(APIView):
    def get(self,request):
        test.delay()
        return Response("success")


