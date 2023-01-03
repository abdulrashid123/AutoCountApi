from rest_framework import serializers
from statement.models import StatementUpload

class StatementUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementUpload
        fields = ['file']