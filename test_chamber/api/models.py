from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    order = models.PositiveIntegerField(default=0, help_text='Порядковый номер шага в курсе.', blank=True)

    class Meta:
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.order:
            last_step = Step.objects.filter(course=self.course).order_by('-order').first()
            if last_step:
                self.order = last_step.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заголовок шага: {self.title} Шаг: {self.order}'


class StepElement(models.Model):
    TYPES = (
        ('TEXT', 'текст'),
        ('TEST', 'тест'),
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='elements')
    order = models.PositiveIntegerField(default=0, help_text='Порядковый номер контента в шаге.', blank=True)
    step_element_type = models.CharField(max_length=10, choices=TYPES)

    class Meta:
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.order:
            last_element = StepElement.objects.filter(step=self.step).order_by('-order').first()
            if last_element:
                self.order = last_element.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заголовок: {self.step.title} Номер: {self.order} Тип: [{self.get_step_element_type_display()}]'


class TextElement(models.Model):
    step_element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='text_content')
    body = models.TextField(help_text='Текст статьи')

    def clean(self):
        # Защита: контент TEXT не должен быть привязан к элементу типа TEST
        if self.step_element.step_element_type != 'TEXT':
            raise ValidationError("Родительский элемент должен иметь тип 'TEXT'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Принудительно запускаем clean() перед сохранением
        super().save(*args, **kwargs)


# --- БЛОК ТЕСТОВ ---

class TestElement(models.Model):
    step_element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='test_content')
    question = models.CharField(max_length=255)

    def clean(self):
        if self.step_element.step_element_type != 'TEST':
            raise ValidationError("Родительский элемент должен иметь тип 'TEST'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Теперь валидация точно сработает
        super().save(*args, **kwargs)


class TestOption(models.Model):
    test_element = models.ForeignKey(TestElement, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)
    answer = models.TextField()


# --- БЛОК ПРОГРЕССА ---

class UserStepProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_progress')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'step'], name='unique_user_step_progress')
        ]
        
    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
            
        super().save(*args, **kwargs)
