from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Quiz(models.Model):
    QuizId = models.IntegerField()
    QuizName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.QuizId}({self.QuizName})"

class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, blank=True, related_name="questions")
    question = models.CharField(max_length=200)
    q1= models.CharField(max_length=200)
    q2= models.CharField(max_length=200)
    q3= models.CharField(max_length=200)
    q4= models.CharField(max_length=200)
    a = models.CharField(max_length=1)


    def __str__(self):
        return f"{self.id}"

class Scores(models.Model):
         
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    score = models.IntegerField()






