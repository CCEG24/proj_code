from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@login_required(login_url='accounts:login')
def comment_wall_view(request):
    # Check for comments without users and delete them
    Comment.objects.filter(user__isnull=True).delete()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create comment instance but don't save yet
            comment = form.save(commit=False)
            
            # Associate user if authenticated
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                messages.error(request, 'You must be logged in to post comments.')
                return redirect('comments:comment_wall')

            # Check for parent comment (if it's a reply)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    messages.error(request, 'The comment you are replying to no longer exists.')
                    return redirect('comments:comment_wall')

            comment.save()
            messages.success(request, 'Comment posted successfully!')
            return redirect('comments:comment_wall')
    else:
        form = CommentForm()
    
    # Fetch only top-level comments (comments with no parent)
    comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    
    context = {
        'form': form,
        'comments': comments,
    }
    
    return render(request, 'comments/comment_wall.html', context)
