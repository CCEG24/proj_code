from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout as auth_logout

def logout(request):
    # Clear any session-related data before logging out
    for key in list(request.session.keys()):
        if key.startswith('voted_'):
            del request.session[key]
    auth_logout(request)  # Log the user out
    return HttpResponseRedirect(reverse('polls:index'))

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not request.user.is_superuser:
        
        if f'voted_{question_id}' in request.session:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You've already voted on this poll.",
                'redirect_url': '/polls/'
            })
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Mark this poll as voted in the session
        if not request.user.is_superuser:
            request.session[f'voted_{question_id}'] = True
            print(f"Session Data: {request.session.items()}")
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))