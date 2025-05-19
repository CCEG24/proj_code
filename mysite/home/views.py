from django.shortcuts import render

# Create your views here.

def index(request):
    """Render the main index page"""
    context = {
        'is_superuser': request.user.is_superuser,
        'username': request.user.username if request.user.is_authenticated else None
    }
    return render(request, 'home/index.html', context)
