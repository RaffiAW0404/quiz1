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
oRecord = {"Number": 0,"Primes":0,"Geometry":0,"Angles":0,"Trigonometry":0,"3D shapes":0,"Fractions":0,"Ratio":0,"Combinations/Probability":0,"Averages/Percentages":0,"Logic":0,"Equations":0,"Circles":0,"Indices/Surds":0}
topics = []
for i in oRecord:
    topics.append(i)

# Create your views here.

#function to render the choose quiz page
def cc1(request):
    return render(request, "question/cc1.html")

def cc2(request):
    return render(request, "question/cc2.html",{
        "topics": topics
    })

def cc3(request):
    return render(request, "question/cc3.html")

#function to render each question
def ques(request, question_id):
    question = Question.objects.get(id=question_id)
    photo = question.diagram.url
    print(photo)
    return render(request, "question/ques.html", {  #of trying to mark it
        "question": question,
        "photo": photo
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
    user = request.user
    
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
        request.session["curQuizIDs"].append(question.id)         
        t = question.topic
        request.session["ansRecord"] = user.get_ansRecord()
        request.session["ansRecord"][t] += 1
        user.set_ansRecord(request.session["ansRecord"])
        user.save()
        if request.POST["question"] == ans:
            request.session["points"]+=4
            request.session["tickRecord"] = user.get_tickRecord()
            request.session["tickRecord"][t] += 1
            user.set_tickRecord(request.session["tickRecord"])
            user.save()
        else:
            request.session["points"]+=-1
            request.session["curQuizQues"].append(question.question)
            a=question.a
            request.session["curQuizAns"].append(eval(f"question.q{a}"))
        
        if request.session["count"] == (num):                          #num is the length of the quiz so if reached need to break out
            return HttpResponseRedirect(reverse("end"))
            

        else:
            #render next quesion in quiz
            nextQuestion = Question.objects.get(id=int(request.session["qs"][request.session["count"]]))
            print(nextQuestion.question)
            request.session["count"]+=1
            try:
                photo = nextQuestion.diagram.url
                print(photo)
                return render(request, "question/ques.html", {  #of trying to mark it
                    "question": nextQuestion,
                    "photo": photo
                })
            except ValueError:
                return render(request, "question/ques.html", {  #of trying to mark it
                    "question": nextQuestion
                })

def end(request):
    quiz = Quiz.objects.get(id=request.session["curId"])
    # try:
    #     lead = Scores.objects.filter(quiz=quiz, user=request.user).order_by("-score")[0]
    #     print(lead)
    #     leadScore = lead.score
    # except IndexError:                          #if this is the first attempt there is no data matching query
    #     leadScore = 0                           #so we make an exception
    
    lead = Scores.objects.filter(quiz=quiz, user=request.user).order_by("-score")
    if lead:
        lead = Scores.objects.filter(quiz=quiz, user=request.user).order_by("-score")[0]
        leadScore = lead.score
    else:
        leadScore = 0


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
        "ques": request.session["curQuizIDs"],
    })

def feedback(request,question_id):
    q = Question.objects.get(id=question_id)
    a = q.a
    ans = eval(f"q.q{a}")
    sol = q.solutionImg.url
    return render(request,"question/feedback.html",{
        "question": q,
        "answer": ans,
        "solution": sol
    })


#function called when link to quiz pressed
#loads up quiz
def start(request, quiz_id):
    #set up variables and arrays required for attempt at quiz
    request.session["qs"] = []
    request.session["curQuizIDs"]=[]
    request.session["curQuizQues"]=[]
    request.session["curQuizAns"]=[]

    request.session["count"] = 0
    request.session["points"] = 25
    request.session["curId"] = quiz_id

    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    for question in questions:
        request.session["qs"].append(question.id)                          
    num = len(request.session["qs"])                               #creates list of all question ids and length
    return render(request, "question/start.html", {  #render start page of quiz
        "quiz": quiz,
        "startQuestion": request.session["qs"][0]
    })

def startTopic(request, topic):
    request.session["qs"] = []
    request.session["curQuizIDs"]=[]
    request.session["curQuizQues"]=[]
    request.session["curQuizAns"]=[]

    request.session["count"] = 0
    request.session["points"] = 25
    request.session["topic"] = topic

    questions = Question.objects.filter(topic=topic)
    for question in questions:
        request.session["qs"].append(question.id)
    print(request.session["qs"][0])
    return render(request, "question/startTopic.html",{
        "startQuestion": request.session["qs"][0],
        "topic": topic,
        
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
    global oRecord

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
            user.set_tickRecord(oRecord)
            user.set_ansRecord(oRecord)
            user.save()                                     #save's new details to databas
            return HttpResponseRedirect(reverse("login"))   #and redirects them to login page

    return render(request, "users/signUp.html")

#function to allow user to change password
def change(request):
    if request.method == "POST":
        username = request.POST["username"]
        password0 = request.POST["password0"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        user = authenticate(request, username=username, password=password0) #checks user's credentials
        if user is not None:
            if password1 == password2:
                return render(request, "question/profile.html")   #if correct proceeds them to site
        else:
            return render(request, "users/change.html", {
                "message": "Invalid credentials"
            })                                              #if not makes them re-enter

    return render(request, "users/change.html")

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
    q = Quiz.objects.get(id=quiz_id)
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
    if request.user not in people:
        for i in range(len(Scores.objects.filter(quiz=q))):
            x = Scores.objects.filter(quiz=q).order_by("-score")[i]
            if x.user == request.user:
                num = i
                userBest = x
                return render(request, "question/lead.html",{
                    "lead": best,
                    "quiz": q,
                    "num": num,
                    "userBest": userBest
                })

    return render(request, "question/lead.html",{
        "lead": best,
        "quiz": q,
    })

#function to render profile page
def profile(request):
    user = request.user
    request.session["ansRecord"] = user.get_ansRecord()
    request.session["tickRecord"] = user.get_tickRecord()
    request.session["record"] = {}
    topics = []
    for j in request.session["ansRecord"]:
        topics.append(j)
    for i in range(len(request.session["tickRecord"])):
        try:
            request.session["percent"] = round((request.session["tickRecord"][topics[i]])/(request.session["ansRecord"][topics[i]]),2)
        except ZeroDivisionError:
            request.session["percent"] = 0
        request.session["record"][topics[i]] = str(round(request.session["percent"]*100,2))+"%"
    print(request.session["record"])
    return render(request, "question/profile.html",{
        "user": request.user,
        "record": request.session["record"]
    })

def create(request):
    return render(request, "question/create.html")

def createq(request):
    if request.method == "POST":
        q = request.POST["question"]
        q1 = request.POST["q1"]
        q2 = request.POST["q2"]
        q3 = request.POST["q3"]
        q4 = request.POST["q4"]
        q5 = request.POST["q5"]
        ans = request.POST["ans"]
        topic = request.POST["topic"]
        solution = request.POST["solution"]
        quiz = Quiz.objects.filter(id=request.POST["quiz"])
        print(quiz)

        

        if int(ans) < 1 or int(ans) > 5:
            message = "Answer must be either option 1,2,3,4 or 5"
            return render(request, "question/createq.html",{
                "message": message
            })
        if topic not in topics:
            message = "Invalid topic"
            return render(request, "question/createq.html",{
                "message": message
            })
        if not quiz:
            message = "Please enter a valid quiz id"
            return render(request, "question/createq.html",{
                "message": message
            })

        question = Question(question=q,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,a=ans,topic=topic,solution=solution)
        question.save()
        question.quiz.add(quiz[0])
        question.save()
        message = "Question created succesfully"
        return render(request, "question/createq.html",{
                "message": message
            })
    return render(request, "question/createq.html")

def buildq(request):
    if request.method == "POST":
        name = request.POST["name"]
        quiz = Quiz(QuizName=name,average=0,totalScore=0,totalAttempts=0)
        quiz.save()
    return render(request, "question/buildq.html")