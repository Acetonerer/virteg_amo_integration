from django.db import models


class Document:
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
