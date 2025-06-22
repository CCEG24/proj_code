from django.shortcuts import render
from .services import handle_question

# Create your views here.
def index(request):
    answer = None
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            answer = handle_question()
    return render(request, 'question_bot/questionanswerer.html', {'answer': answer})