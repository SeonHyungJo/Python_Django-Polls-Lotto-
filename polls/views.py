from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic

# Create your views here.
from .models import Question, Choice
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
         selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except:
         return render(request, 'polls/detail.html', {
             'question': question,
             'error_message': "You didn't select a choice."
         })
    else:
         selected_choice.vote +=1
         selected_choice.save()
         return redirect('polls:results', pk = question.id)

def main(request):
    return render(request, 'polls/main.html')
