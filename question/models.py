from django.db import models

# Create your models here.

class Quiz(models.Model):
    QuizId = models.IntegerField()
    QuizName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.QuizId}({self.QuizName})"

class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, blank=True, related_name="questions")
    question = models.CharField(max_length=200)
    qa= models.CharField(max_length=200)
    qb= models.CharField(max_length=200)
    qc= models.CharField(max_length=200)
    qd= models.CharField(max_length=200)
    a = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.id}"






