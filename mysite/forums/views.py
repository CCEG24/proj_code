from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Thread, Post
from .forms import PostForm, ThreadForm
from django.db import models
from django.contrib import messages

# Create your views here.

@login_required
def forum_list(request):
    if request.user.is_superuser:
        threads = Thread.objects.all().order_by('-created_at')
    else:
        threads = Thread.objects.filter(
            models.Q(visibility='public') | models.Q(user=request.user)
        ).order_by('-created_at').distinct()
    return render(request, 'forums/forum_list.html', {'threads': threads})

@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    
    posts = thread.posts.filter(parent__isnull=True).order_by('created_at') # Get top-level posts

    if request.user.is_authenticated:
        pass
    else:
        return redirect('accounts:login')

    # Restrict posting to verified users
    if request.method == 'POST':
        if not request.user.profile.is_email_verified:
            messages.error(request, 'You must verify your email to post in the forums.')
            return redirect('forums:thread_detail', pk=thread.pk)
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.thread = thread
            new_post.user = request.user
            # Handle replies - if a post_id is provided in the form
            if 'parent_id' in request.POST:
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    try:
                        new_post.parent = Post.objects.get(pk=parent_id)
                    except Post.DoesNotExist:
                        pass # Or handle invalid parent_id
            new_post.save()
            return redirect('forums:thread_detail', pk=thread.pk)
    else:
        form = PostForm()

    return render(request, 'forums/thread_detail.html', {
        'thread': thread,
        'posts': posts,
        'form': form
    })

@login_required
def create_thread(request):
    # Restrict thread creation to verified users
    if not request.user.profile.is_email_verified:
        messages.error(request, 'You must verify your email to create a thread.')
        return redirect('forums:forum_list')
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_thread = form.save(commit=False)
            new_thread.user = request.user
            new_thread.save()
            return redirect('forums:forum_list') # Redirect to the forum list after creating a thread
    else:
        form = ThreadForm()
    return render(request, 'forums/create_thread.html', {'form': form})
