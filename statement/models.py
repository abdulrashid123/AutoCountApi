from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bank(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class StatementUpload(models.Model):
    bank = models.ForeignKey(Bank,blank=True,null=True,on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    parse = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    errorMessage = models.CharField(max_length=3000,blank=True,null=True)
    startDate = models.DateField(blank=True,null=True)
    endDate = models.DateField(blank=True,null=True)
    createdDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Statement(models.Model):
    bank = models.ForeignKey(Bank,blank=True,null=True,on_delete=models.CASCADE)
    statementUpload = models.ForeignKey(StatementUpload,blank=True,null=True,on_delete=models.CASCADE)
    date = models.DateField(blank=True,null=True)
    description = models.CharField(max_length=2000,blank=True,null=True)
    reference = models.CharField(max_length=200,blank=True,null=True)
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return str(self.date)



class Transaction(models.Model):
    statement = models.ForeignKey(Statement,blank=True,null=True,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    createdDate = models.DateField(auto_now_add=True)
    invoiceId = models.CharField(max_length=200,blank=True,null=True)



@receiver(post_save, sender=Transaction)
def update_transaction(sender, instance, **kwargs):
    balance = instance.statement.balance
    amount = instance.amount
    statement = instance.statement
    statement.balance = balance - amount
    if statement.balance <= 0:
        statement.paid = True
    statement.save()


