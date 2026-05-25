from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'имя юзера: {self.username}'

# --- БЛОК КУРСА ---

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Step(models.Model):
    class StepType(models.TextChoices):
        TEXT = 'TEXT', 'Текст'
        TEST = 'TEST', 'Тест'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    step_type = models.CharField(max_length=10, choices=StepType.choices)
    order = models.PositiveIntegerField(help_text="Порядковый номер шага в курсе")
    text_content = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order') 

    def check(self):
        # Защита от дурака: проверяем логику полей перед сохранением
        if self.step_type == self.StepType.TEXT and not self.text_content:
            raise ValidationError("Для текстового шага необходимо заполнить text_content.")
        if self.step_type == self.StepType.TEST and self.text_content:
            raise ValidationError("Тестовый шаг не должен содержать лекционный текст.")

    def __str__(self):
        return f"{self.course.title} - Шаг {self.order}: {self.title}"


# --- БЛОК ТЕСТОВ ---

class Question(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="Текст вопроса")

    def check(self):
        # Проверяем, что вопрос привязывают именно к тестовому шагу
        if self.step.step_type != Step.StepType.TEST:
            raise ValidationError("Нельзя добавить вопрос к текстовому шагу курса.")

    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, help_text="Является ли ответ правильным")

    def __str__(self):
        return self.text


# --- БЛОК ПРОГРЕССА ---

class UserStepProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_progress')
    # Защищаем прогресс от случайного удаления курса/шага администратором
    step = models.ForeignKey(Step, on_delete=models.PROTECT, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    # Храним процент правильных ответов, если это был тест
    score = models.PositiveIntegerField(blank=True, null=True, help_text="Балл за тест (в %)")
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'step')
