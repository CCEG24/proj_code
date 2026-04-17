import time

from django.shortcuts import render

from .forms import QuestionForm
from .services import handle_question

# Create your views here.
def reverse_text(value, should_reverse):
    if not value:
        return value
    return value[::-1] if should_reverse else value


def index(request):
    answer = None
    errorMessage = None
    questionValue = ''
    form = QuestionForm(request.POST or None)
    if request.method == 'POST':
        questionValue = request.POST.get('question', '')
        if form.is_valid():
            answer = handle_question(form.cleaned_data['question'])
        else:
            errorMessage = 'Use proper grammar and end your question with a question mark.'

    is_april_fools = time.strftime("%m-%d") == "04-01"
    context = {
        'answer': reverse_text(answer, is_april_fools),
        'errorMessage': reverse_text(errorMessage, is_april_fools),
        'isAprilFools': is_april_fools,
        'pageTitle': reverse_text('Question Answerer 5000', is_april_fools),
        'pageHeader': reverse_text('Question Answerer 5000', is_april_fools),
        'questionLabel': reverse_text("Ask your question! Must have a question mark at the end >:(. Use 'calculate [maths question]' to do maths!", is_april_fools),
        'noteText': reverse_text("Note: This is a joke and the answer is not always correct (unless you're doing maths).", is_april_fools),
        'buttonText': reverse_text('Ask', is_april_fools),
        'answerLabel': reverse_text('Answer:', is_april_fools),
        'placeholderText': reverse_text('Ask your question here...', is_april_fools),
        'questionValue': questionValue,
        'form': form,
    }
    return render(request, 'question_bot/questionanswerer.html', context)