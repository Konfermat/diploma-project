from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

# --- БЛОК КУРСА ---
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заголовок урока {self.title} Краткое описание: {self.description[:30]}'

