from django.db import models
from django.contrib.auth.models import AbstractUser

# null=True, blank=True # для чисел
# blank=True # для текста       

# --- БЛОК ЮЗЕРА ---
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    # список пройденных уроков
    completed_lessons = models.ManyToManyField(
        'Lesson', 
        blank=True, 
        related_name='completed_by',
        verbose_name="Пройденные уроки"
    )    

# --- БЛОК УРОКА ---
class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    is_published = models.BooleanField(default=False)
    

class LessonPart(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='parts')
    title = models.CharField(max_length=255, verbose_name="Название части")
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['lesson', 'order'], name='unique_part_order')
        ]        
        


# --- БЛОК ТЕКСТА ---
class Text(models.Model):
    lesson_part = models.ForeignKey(LessonPart, on_delete=models.CASCADE, related_name='texts', null=True, blank=True)
    lesson_material = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['lesson_part', 'order'], name='unique_text_order')
        ]        


# --- БЛОК ТЕСТА ---
class Test(models.Model):
    lesson_part = models.ForeignKey(LessonPart, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    question = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['lesson_part', 'order'], name='unique_test_order')
        ]        
class TestOption(models.Model):
    option = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order', 'id']

# --- БЛОК ПРОГРЕССА ---
class UserTestAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_answers')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(TestOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name="Правильно ли ответил")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'test'], name='unique_user_test_attempt')
        ]

