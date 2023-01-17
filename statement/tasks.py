from celery import shared_task
from datetime import datetime
from Parser.Hdfc import Hdfc
from statement.models import StatementUpload,Statement,Bank
from django.conf import settings
import os
from pathlib import Path

@shared_task(bind=True)
def test(self,args):
    print(args)
    return "Done"



@shared_task(bind=True)
def parseStatement(self,*args):
    file = args[0][1:]
    filepath = os.path.join(Path(__file__).resolve().parent.parent,file)

    bank = args[1]

    bank_obj = Bank.objects.get(name=bank[0])
    stat_bank_upl_obj = StatementUpload.objects.get(id=args[2])
    try:
        instance = eval(bank[0])(filepath)
        rows_statements = instance.parse_statement(bank_obj,stat_bank_upl_obj)
        msg = Statement.objects.bulk_create(rows_statements)
        print(msg)
    except Exception as e:
        print(e)
    return "Done"