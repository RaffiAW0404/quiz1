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
# def qz(request, quiz_id):
#     quiz = Quiz.objects.get(QuizId=quiz_id)
#     return render(request, "question/qz.html", {
#         "quiz": quiz,
#         "questions": quiz.questions.all(),
#         "non_questions": Question.objects.exclude(quiz=quiz).all()
#     })


#old function
# def check(request, quiz_id):
#     if request.method == "POST":
#         print(quiz_id)
#         quiz = Quiz.objects.get(QuizId=quiz_id)
#         questions = quiz.questions.all()
#         answers=[]
#         num = 0
#         for i in questions:
#            answers.append(i.a)
#            num += 1

#         for j in range(num):
#             print(j)
#             print(answers)
#             answer = "option"+answers[int(j)]
#             print(answer)
#             print(request.POST["question"])
#             if request.POST["question"] == answer:
#                 print("correct")
#             else:
#                 print("incorrect")

#         # print(answers)
#         # answer = "option"+answers[0]
#         # print(answer)
#         # #for j in answers:
            
#         #    # print(j)
#         # print(request.POST["question"])
#         # if request.POST["question"] == answer:
#         #     print("correct")
#         # else:
#         #     print("incorrect")
#         # option = Question.objects.get(id=int(request.POST["question"]))

#function to render each question
def ques(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "question/ques.html", {
        "question": question 
    })

#function to check submitted question
def qcheck(request, question_id):
    print(request.session)
    # global points
    # global qs
    # global num
    # global count
    # global curId
    # global curQuizCorrect


    print(request.session["qs"][0])
    print(question_id)
    
    num = len(request.session["qs"])
    
    if request.session["count"] == 0:                                      #qcheck is first called by startQuiz button 
        firstQuestion = Question.objects.get(id=request.session["qs"][0])  #this if statement ensures that on the 1st time
        request.session["count"] += 1                                      #it is called it renders the first question instead
        try:
            photo = firstQuestion.diagram.url
            print(photo)
            return render(request, "question/ques.html", {  #of trying to mark it
                "question": firstQuestion,
                "photo": photo
            })
        except ValueError:
            return render(request, "question/ques.html", {  #of trying to mark it
                "question": firstQuestion
            })
    else:                                               
        question = Question.objects.get(id=question_id)
        ans = "option"+question.a                       #checkboxes are posted with option at the beginning 
        if request.POST["question"] == ans:
            request.session["points"]+=1
        else:
            request.session["curQuizIDs"].append(question.id)          #adds points if answer correct
            request.session["curQuizQues"].append(question.question)
            a=question.a
            request.session["curQuizAns"].append(eval(f"question.q{a}"))
        
        if request.session["count"] == (num):                          #num is the length of the quiz so if reached need to break out
            quiz = Quiz.objects.get(QuizId=request.session["curId"])
            try:
                lead = Scores.objects.filter(quiz=quiz, user=request.user).order_by("-score")[0]
                print(lead)
                leadScore = lead.score
            except IndexError:                          #if this is the first attempt there is no data matching query
                leadScore = 0                           #so we make an exception


            entry = Scores(quiz=quiz, user=request.user, score=request.session["points"])
            entry.save()                                #save current attempt

            
            #display a message based off how the user performed in relation to their highscore
            if request.session["points"] == leadScore:
                if len(Scores.objects.filter(quiz=quiz, user=request.user)) > 1:
                    message = "Congratulations you have equalled your highscore of "+str(leadScore)+" points!"
                else:
                    message = "Congratulations you have a set a highscore of "+str(request.session["points"])+" points!"
            elif request.session["points"] > leadScore:
                message = "Congratulations you have beaten your highscore of "+str(leadScore)+" points with an awesome score of "+str(request.session["points"])+" !"
            else:
                message = "Unlucky you didnt quite reach your highscore of "+str(leadScore)+" points with your score of "+str(request.session["points"])+". Better luck next time!"
                        
            return render(request, "question/end.html", {
                "message": message,
                "quiz": quiz,
                "quesWrong": request.session["curQuizIDs"],
                "quesWrongQues": request.session["curQuizQues"],
                "quesWrongAns": request.session["curQuizAns"]
            })

        else:
            #render next quesion in quiz
            nextQuestion = Question.objects.get(id=int(request.session["qs"][request.session["count"]]))
            print(nextQuestion)
            request.session["count"]+=1
            return render(request, "question/ques.html" , {
                "question": nextQuestion 
            })

#function called when link to quiz pressed
#loads up quiz
def start(request, quiz_id):
    # global num
    # global qs
    # global count
    # global curId
    # global points
    # global curQuizCorrect

    #set up variables and arrays required for attempt at quiz
    request.session["qs"] = []
    request.session["curQuizIDs"]=[]
    request.session["curQuizQues"]=[]
    request.session["curQuizAns"]=[]

    request.session["count"] = 0
    request.session["points"] = 0
    request.session["curId"] = quiz_id

    quiz = Quiz.objects.get(QuizId=quiz_id)
    questions = quiz.questions.all()
    for question in questions:
        request.session["qs"].append(question.id)                          
    num = len(request.session["qs"])                               #creates list of all question ids and length
    return render(request, "question/start.html", {  #render start page of quiz
        "quiz": quiz,
        "question1": request.session["qs"][0]
    })

def index(request):
    if request.user.is_authenticated:                   #checks if user is logged in and if not
        return render(request, "question/index.html")   #forces them to do so
    else:
        return HttpResponseRedirect(reverse("welcome"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) #checks user's credentials
        if user is not None:
            login(request, user)
            return render(request, "question/index.html")   #if correct proceeds them to site
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })                                              #if not makes them re-enter

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
        #password validation here currently disabled during development(for main site) phase
        check = User.objects.filter(username=username)  #checks if the username is taken and 
        if len(check) == 1:                             #if so forces user to choose another
            return render(request, "users/signUp.html",{
                "message": "Username already taken"
            })
        else:
            user = User(username=username)
            user.set_password(password)
            user.save()                                     #save's new details to databas
            return HttpResponseRedirect(reverse("login"))   #and redirects them to login page

    return render(request, "users/signUp.html")

#function to render welcome page
def welcome_view(request):
    return render(request,"users/welcome.html")

#function to log user out
def logout_view(request):
    logout(request)
    return render(request, "users/welcome.html", {
        "message": "Logged Out"
    })

#function to render page to view choice of leaderboards
def leads(request):
    return render(request, "question/leads.html")

#function to render a leaderboard
def lead(request, quiz_id):
    q = Quiz.objects.get(QuizId=quiz_id)
    people=[]
    best=[]
    flag = True
    i=0
    #this while loop creates a list of the top 10(or less) scores for that quiz
    while flag == True and i < len(Scores.objects.filter(quiz=q)):
        top = Scores.objects.filter(quiz=q).order_by("-score")[i]
        #queries the database for the 'ith' index of all the ojects stored in Scores
        #for this quiz ordered by highest score in descending order
        person = top.user
        i+=1
        if person in people:            #checks if the user of this score is already in list
            if i < len(Scores.objects.filter(quiz=q)):
                top = Scores.objects.filter(quiz=q).order_by("-score")[i]
            else:
                flag=False
            #if they are then fetch the next score in the the list if it exists
        else:
            people.append(person)
            best.append(top)
            #add user to the list of people in the list adn add score to leaderboard
        if len(best) >= 10:
            flag = False
            #if 10 scores list break out of loop
    return render(request, "question/lead.html",{
        "lead": best,
        "quiz": q
    })

#function to allow user to change password
def change(request):
    pass

#function to render profile page
def profile(request):
    return render(request, "question/profile.html",{
        "user": request.user
    })