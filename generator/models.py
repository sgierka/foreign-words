from django.db import models


# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class Meaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning_id = models.AutoField(primary_key=True)
    meaning = models.TextField()

    def __str__(self):
        return self.meaning
