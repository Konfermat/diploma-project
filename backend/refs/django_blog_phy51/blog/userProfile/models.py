from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True, verbose_name='Заблокирован до')
    is_moderator = models.BooleanField(default=False)

    def is_currently_blocked(self):
        if not self.is_blocked:
            return False
        if self.blocked_until and timezone.now() > self.blocked_until:
            self.is_blocked = False
            self.blocked_until = None
            self.save()
            return False
        return True

    def __str__(self):
        return self.user.username

