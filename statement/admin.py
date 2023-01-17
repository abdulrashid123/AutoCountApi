from django.contrib import admin
from statement.models import StatementUpload,Statement,Bank,Transaction

admin.site.register([StatementUpload,Statement,Bank,Transaction])
