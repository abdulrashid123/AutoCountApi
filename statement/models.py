from django.db import models
from django.contrib.auth.models import User

class StatementUpload(models.Model):

    file = models.FileField(blank=True, null=True)
    parse = models.BooleanField(default=False)