from rest_framework import serializers
from statement.models import StatementUpload,Statement,Bank,Transaction

class StatementUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementUpload
        fields = '__all__'
        depth=1

class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        depth = 1
        fields = '__all__'

