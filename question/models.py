from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
#inherits from default django user model to allow me to link self-made models with it

#creates table that stores data for each quiz
class Quiz(models.Model):
    QuizId = models.IntegerField()
    QuizName = models.CharField(max_length=50)
    average = models.IntegerField()
    totalScore = models.IntegerField()
    totalAttempts = models.IntegerField()

#creates table that stores data for each question 
class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, blank=True, related_name="questions")
    #the many to many field here creates a new table to link the question and quiz tables
    #this means that a quiz can contain many questions and a question can belong to many quizzes
    question = models.CharField(max_length=500)
    q1= models.CharField(max_length=200)
    q2= models.CharField(max_length=200)
    q3= models.CharField(max_length=200)
    q4= models.CharField(max_length=200)
    q5= models.CharField(max_length=200)
    a = models.CharField(max_length=1)
    diagram = models.ImageField(blank=True,upload_to='photos')

#creates table that stores data for each score(when a user completes a quiz)
class Scores(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    #these foriegn keys allow the scores table to reference and link to a record in the quiz 
    #and user tables respectively
    score = models.IntegerField()
