from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Answer, Question
from Algorithm.polls.question_match import Question_Match

# class IndexView(generic.ListView):
#     template_name = 'polls/home.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:10]

def HomeView(request):
    all_question_list=Question.objects.order_by('-pub_date')
    pub_question_list=Question.objects.order_by('-matched_nums')[:5]
    try:
        original_question = request.POST['original_question']      
    except Exception:     
        return render(request, 'polls/home.html',{'pub_question_list':pub_question_list})
    if len(original_question)!=0:
        matched_questions=Question_Match(original_question,all_question_list,4)
        return render(request, 'polls/home.html',{'matched_question_list':matched_questions,
        'pub_question_list':pub_question_list})
    else:
        return render(request, 'polls/home.html',{'pub_question_list':pub_question_list})
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


