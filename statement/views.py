from rest_framework import generics
from .serializers import StatementUploadSerializer
from .models import StatementUpload
from rest_framework.response import Response
from rest_framework import status


class PDFFileCreateView(generics.CreateAPIView):
    queryset = StatementUpload.objects.all()
    serializer_class = StatementUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("https://stackoverflow.com/questions/45398323/django-str-object-has-no-attribute-values-in-rest-framework", status=status.HTTP_201_CREATED, headers=headers)
