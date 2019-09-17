from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
# Create your views here.

def index(request):
    latist_question_list = Question.objects.all.order_by('-pub_date')[:5]
    content = {
        'latist_question_list':latist_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def vote(request,question_id):
    