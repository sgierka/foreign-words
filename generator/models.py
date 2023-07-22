from django.db import models


# Create your models here.
class KeyModel(models.Model):
    key = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.key_name


class ValueModel(models.Model):
    key_name= models.ForeignKey(KeyModel, on_delete = models.CASCADE)
    value_name = models.CharField(max_length=100)

    def __str__(self):
        return self.value_name

