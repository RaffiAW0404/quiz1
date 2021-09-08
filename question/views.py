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

def check(request, quiz_id):
    if request.method == "POST":
        print(quiz_id)
        quiz = Quiz.objects.get(QuizId=quiz_id)
        questions = quiz.questions.all()
        answers=[]
        num = 0
        for i in questions:
           answers.append(i.a)
           num += 1

        for j in range(num):
            print(j)
            print(answers)
            answer = "option"+answers[int(j)]
            print(answer)
            print(request.POST["question"])
            if request.POST["question"] == answer:
                print("correct")
            else:
                print("incorrect")

        # print(answers)
        # answer = "option"+answers[0]
        # print(answer)
        # #for j in answers:
            
        #    # print(j)
        # print(request.POST["question"])
        # if request.POST["question"] == answer:
        #     print("correct")
        # else:
        #     print("incorrect")
        # option = Question.objects.get(id=int(request.POST["question"]))

