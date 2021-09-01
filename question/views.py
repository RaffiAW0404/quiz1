from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    return render(request, "question/index.html")

def cc1(request):
    return render(request, "question/cc1.html")

def qz(request, quiz_id):
    quiz = Quiz.objects.get(QuizId=quiz_id)
    return render(request, "question/qz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all(),
        "non_questions": Question.objects.exclude(quiz=quiz).all()
    })