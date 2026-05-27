from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    Здесь я напишу какой основной логикой руководствуется моя БД.

    Курс это список шагов. Шаги в свою очередь привязаны к курсу, содержат
    списки текстов и список тестов.
    Тесты привязаны к шагу


    Основная структура такая:
    # БЛОК КУРСОВ
        Course
            Курс "содержит": 
                описание,
                список шагов (Step)
        Step
            Каждый шаг может содержать:
                список текстов или список контента (StepContent),
                список тестов (Test)
        StepContent
            текстовый контент шага # сделан отдельный класс для правильногшо структурирования

    # БЛОК ТЕСТОВ
        Test
            Тест содержит:
                вопрос
                список возможных ответов (TestOpiton)
        TestOption
            текст варианта ответа 

    # БЛОК ПРОГРЕССА
        User
        UserStepProgress
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

class StepContent(models.Model):
    # название переменной будет step потому что так принято?
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='contents')
    material = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(help_text='Порядковый номер контента в шаге.')

    class Meta:
        ordering = ['order']
        unique_together = ('step', 'order') 

# --- БЛОК ТЕСТОВ ---

class Test(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='tests')
    question = models.CharField(max_length=255)

class TestOption(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False, help_text='Является ли ответ правильным')
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

