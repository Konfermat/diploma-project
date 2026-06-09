from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

''' 
    Рубрика "ИИ сказала..."
        Архитектурное правило DRF 
        Базовая валидация (БД): 
        Уникальность, типы данных и связи 
        (как ваши UniqueConstraint в Step и StepElement) 
        должны оставаться в модели. 
        DRF автоматически подхватит их и превратит в ошибки валидации.
        Бизнес-логика: 
        Сложные проверки (например, "нельзя добавить тест, 
        если в шаге уже есть 5 элементов" или проверка дат) 
        переносятся в Сериализатор.
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заголовок курса {self.title} Краткое описание: {self.description[:30]}'

class Step(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(help_text='Порядковый номер шага в курсе.')

    class Meta:
        ordering = ['order']

        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_course_step_order')
        ]

    def __str__(self):
        return f'Заголовок шага: {self.title} Шаг: {self.order}'

class StepElement(models.Model):
    TYPES = (
        ('TEXT', 'текст'),
        ('TEST', 'тест'),
    )

    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='elements')
    order = models.PositiveIntegerField(help_text='Порядковый номер контента в шаге.', null=True, blank=True)
    step_element_type = models.CharField(max_length=10, choices=TYPES)

    class Meta:
        ordering = ['order']

        constraints = [
            models.UniqueConstraint(fields=['step', 'order'], name='unique_step_element_order')
        ]        

    def __str__(self):
        return f'Заголовок: {self.step.title} Номер: {self.order} Тип: [{self.get_step_element_type_display()}]' 

class TextElement(models.Model):
    step_element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='text_content')
    body = models.TextField(help_text='Текст статьи')

# --- БЛОК ТЕСТОВ ---

class TestElement(models.Model):
    step_element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='test_content')
    question = models.CharField(max_length=255)

    def clean(self):
        # Защита: контент TEST не должен быть привязан к элементу типа TEXT
        if self.step_element.step_element_type != 'TEST':
            raise ValidationError("Родительский элемент должен иметь тип 'TEST'.")

class TestOption(models.Model):
    test_element = models.ForeignKey(TestElement, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)
    answer = models.TextField()


# --- БЛОК ПРОГРЕССА ---



# модель под вопросом
class UserStepProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_progress')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'step'], name='unique_user_step_progress')
        ]
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Автоматически ставим дату, только если шаг пройден и дата еще не установлена
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
            
        # Передаем именованные аргументы явно
        super().save(
            force_insert=force_insert, 
            force_update=force_update, 
            using=using, 
            update_fields=update_fields
        )