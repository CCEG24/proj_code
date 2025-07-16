from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create missing UserProfile objects for users'

    def handle(self, *args, **kwargs):
        count = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} missing profiles.'))
