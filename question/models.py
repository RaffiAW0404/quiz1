from django.db import models

# Create your models here.
class QnA(models.Model):
    questionID = models.IntegerField()
    q = models.CharField(max_length=200)
    a = models.CharField(max_length=200)

class Quizzes(models.Model):
    questionID = models.ForeignKey(QnA, on_delete=models.CASCADE, related_name="question")
    quizID = models.IntegerField()

