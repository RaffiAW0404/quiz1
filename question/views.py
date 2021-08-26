from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "question/index.html")

def cc1(request):
    return render(request, "question/cc1.html")

def qz1001(request):
    return render(request, "question/qz1001.html")