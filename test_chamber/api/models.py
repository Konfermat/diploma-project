from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    Здесь я напишу какой основной логикой руководствуется моя БД.
'''

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Имя юзера: {self.username}'

# --- БЛОК КУРСА ---

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заголовок курса {self.title} Краткое описание: {self.description[:30]}'

class Step(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(help_text='Порядковый номер шага в курсе.')

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order') 

    def __str__(self):
        return f'{self.course.title} - Шаг {self.order}: {self.title}'

class StepElement(models.Model):
    TYPES = (
        ('TEXT', 'текст'),
        ('TEST', 'тест'),
    )

    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='elements')
    order = models.PositiveIntegerField(help_text='Порядковый номер контента в шаге.')
    step_element_type = models.CharField(max_length=10, choices=TYPES)

    class Meta:
        ordering = ['order']
        unique_together = ('step', 'order') 

    def __str__(self):
        return f'{self.step.title} | Элемент {self.order} [{self.get_step_element_type_display()}]'        

class TextContent(models.Model):
    # Связь один-к-одному гарантирует: один элемент = один текст
    element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='text_data')
    material = models.TextField()

# --- БЛОК ТЕСТОВ ---

class Test(models.Model):
    # Один элемент = один вопрос теста
    element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='test_data')
    question = models.CharField(max_length=255)

class TestOption(models.Model):
    # Теперь варианты ответов железно привязаны только к Тестам
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)
    answer = models.CharField(max_length=500)

# --- БЛОК ПРОГРЕССА ---

class UserStepProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_progress')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(blank=True, null=True, help_text='Балл за тест (в %)')
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'step')

# https://share.google/aimode/B2g3JVUP0B1MihcwR
