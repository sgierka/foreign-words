from django.db import models


# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class Meaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning = models.CharField(max_length=100)

    def __str__(self):
        return self.meaning
