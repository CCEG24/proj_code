from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Comment

@receiver(post_save, sender=User)
def update_comment_usernames(sender, instance, **kwargs):
    """
    Signal to update comments when a user's username changes
    """
    # Update all comments by this user
    Comment.objects.filter(user=instance).update(user=instance) 