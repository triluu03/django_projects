from django.db import models

# Create your models here.

class Board(models.Model):
    size = models.IntegerField(default=50)
    details = models.TextField(default=','.join([""]*(50**2)))