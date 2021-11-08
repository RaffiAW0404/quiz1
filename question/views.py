from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.db.models import Max

from .models import *

points = 0
num = 0
qs = []
count = 0
curId = 0

# Create your views here.

#function to render the choose quiz page
def cc1(request):
    return render(request, "question/cc1.html")

#old function 
def qz(request, quiz_id):
    quiz = Quiz.objects.get(QuizId=quiz_id)
    return render(request, "question/qz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all(),
        "non_questions": Question.objects.exclude(quiz=quiz).all()
    })


#old function
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

#unneccessary function
def ques(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "question/ques.html", {
        "question": question 
    })

#function to check submitted question
def qcheck(request, question_id):
    global points
    global qs
    global num
    global count
    global curId

    print(num)
    print(qs[0])
    print(question_id)
    if count == 0:                                      #qcheck is first called by startQuiz button 
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
            curQuizCorrect.append(question_id)
        else:
            print("incorrect")
        print(points)
        
        
        if count == (num):
            quiz = Quiz.objects.get(QuizId=curId)

            try:
                lead = Scores.objects.filter(quiz=quiz, user=request.user).order_by("-score")[0]
                print(lead)
                leadScore = lead.score
            except IndexError:
                leadScore = 0


            entry = Scores(quiz=quiz, user=request.user, score=points)
            entry.save()

            print(curQuizCorrect)
            
            
            if points == leadScore:
                if len(Scores.objects.filter(quiz=quiz, user=request.user)) > 1:
                    message = "Congratulations you have equalled your highscore of "+str(leadScore)+" points!"
                else:
                    message = "Congratulations you have a set a highscore of "+str(points)+" points!"
            elif points > leadScore:
                message = "Congratulations you have beaten your highscore of "+str(leadScore)+" points with an awesome score of "+str(points)+" !"
            else:
                message = "Unlucky you didnt quite reach your highscore of "+str(leadScore)+" points with your score of "+str(points)+". Better luck next time!"
            return render(request, "question/end.html", {
                "message": message,
                "quiz": quiz
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
    global curQuizCorrect

    qs=[]
    curQuizCorrect=[]

    count = 0
    points = 0
    curId = quiz_id
    quiz = Quiz.objects.get(QuizId=quiz_id)
    questions = quiz.questions.all()
    print(questions)
    for question in questions:
        qs.append(question.id)
    print(qs)
    num = len(qs)
    return render(request, "question/start.html", {
        "quiz": quiz,
        "question1": qs[0]
    })

def index(request):
    if request.user.is_authenticated:
        return render(request, "question/index.html")
    else:
        return HttpResponseRedirect(reverse("welcome"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return HttpResponseRedirect(reverse("home"))
            return render(request, "question/index.html")
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })

    return render(request, "users/login.html")

def signUp(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # try:
        #     validate_password(username,password)
        # except ValidationError:
        #     print(password_validators_help_texts())
        #     return render(request, "users/signUp.html",{
        #         "message": "Password must be at least 8 characters long"
        #     })
        check = User.objects.filter(username=username)
        print(len(check))
        if len(check) == 1:
            return render(request, "users/signUp.html",{
                "message": "Username already taken"
            })
        else:
            user = User(username=username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("login"))

    return render(request, "users/signUp.html")

def welcome_view(request):
    return render(request,"users/welcome.html")

def logout_view(request):
    logout(request)
    return render(request, "users/welcome.html", {
        "message": "Logged Out"
    })

def leads(request):
    return render(request, "question/leads.html")

def lead(request, quiz_id):
    q = Quiz.objects.get(QuizId=quiz_id)
    print(Scores.objects.filter(quiz=q).order_by("-score"))
    people=[]
    best=[]
    flag = True
    i=0
    while flag == True and i < len(Scores.objects.filter(quiz=q)):
        top = Scores.objects.filter(quiz=q).order_by("-score")[i]
        print(top)
        person = top.user
        print(person)
        i+=1
        if person in people:
            if i < len(Scores.objects.filter(quiz=q)):
                top = Scores.objects.filter(quiz=q).order_by("-score")[i]
            else:
                flag=False
        else:
            people.append(person)
            print(people)
            best.append(top)
            print(best)

        if len(best) >= 10:
            flag = False
    print(best)
    return render(request, "question/lead.html",{
        "lead": best,
        "quiz": q
    })


def change(request):
    pass

def profile(request):
    return render(request, "question/profile.html",{
        "user": request.user
    })