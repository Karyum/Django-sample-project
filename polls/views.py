from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
    '''
        for the 404 you could do get_object_or_404(Question, pk=question_id)
        check https://docs.djangoproject.com/en/2.1/intro/tutorial03/#id9
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    '''
        this view is going to look on the post data
        and incerement in the choice that was chosen
    '''
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # the line below is not effiecient cause it's a race condition
        # to avoid it read here:
        # https://docs.djangoproject.com/en/2.1/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
