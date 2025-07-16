from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Vote
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

def logout(request):
    # Clear any session-related data before logging out
    for key in list(request.session.keys()):
        if key.startswith('voted_'):
            del request.session[key]
    auth_logout(request)  # Log the user out
    return HttpResponseRedirect(reverse('polls:index'))

# Apply login_required to the DetailView and ResultsView class-based views
@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

@method_decorator(login_required, name='dispatch')
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Restrict voting to verified users
    if not request.user.profile.is_email_verified:
        messages.error(request, 'You must verify your email to vote in polls.')
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You must verify your email to vote in polls.',
        })

    # Check if the user has already voted on this question
    if Vote.objects.filter(user=request.user, question=question).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have already voted on this poll.",
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
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

        # Create a Vote object to record the user's vote
        Vote.objects.create(user=request.user, question=question)

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))