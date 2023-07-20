from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class Key(models.Model):
    key_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.key_name


class Value(models.Model):
    key = models.ForeignKey(Key, on_delete = models.CASCADE)
    value_name = models.CharField(max_length=100)

    def __str__(self):
        return self.value_name

