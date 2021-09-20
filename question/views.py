from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *

points = 0
num = 0
qs = []
count = 0
curId = 0

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

def ques(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "question/ques.html", {
        "question": question 
    })

def qcheck(request, question_id):
    global points
    global qs
    global num
    global count
    global curId

    print(num)
    print(qs[0])
    print(question_id)
    #for i in range(num):
    if count == 0:
        print("YEs")
        firstQuestion = Question.objects.get(id=qs[0])
        count += 1
        return render(request, "question/ques.html", {
            "question": firstQuestion
        })
    else:
        question = Question.objects.get(id=question_id)
        ans = "option"+question.a
        print(ans)
        if request.POST["question"] == ans:
            print("correct")
            points+=1
        else:
            print("incorrect")
        print(points)
        
        
        if count == (num):
            quiz = Quiz.objects.get(QuizId=curId)
            return render(request, "question/end.html",{
                "points":points,
                "quiz":quiz
            })
        else:
            nextQuestion = Question.objects.get(id=qs[count])
            count+=1
            return render(request, "question/ques.html" , {
                "question": nextQuestion 
            })

def start(request, quiz_id):
    global num
    global qs
    global count
    global curId
    global points

    qs=[]
    count = 0
    points = 0
    curId = quiz_id
    quiz = Quiz.objects.get(QuizId=quiz_id)
    num = quiz.numq
    questions = quiz.questions.all()
    print(questions)
    for question in questions:
        qs.append(question.id)
    print(qs)
    return render(request, "question/start.html", {
        "quiz": quiz,
        "question1": qs[0]
    })