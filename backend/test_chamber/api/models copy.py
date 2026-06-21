from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    Логика моей программы на данном этапе.
        Есть Курс состоящий из Шагов. 
        Каждый Шаг это этап изучения или определенный учебный материал. 
        Каждый шаг имеет свойство.
        Сейчас это или текст или тест по тексту.
        Прогресс прохождения фиксируется посящением.


    Здесь я напишу какой основной логикой руководствуется моя БД?
        Course
            инфо о курсе
        Step(fk=Course='steps')
            инфо о шаге курса
        StepElement(fk=Step, rn_n='elements')
            инфо о типе элемента шага
        # создаешь строку в StepElement, определяешь её тип
        # к одной строке (StepElement) один TextElement
        TextElement(OneToOneField=StepElement, r_n='text_content')
            содержит текст и проверку типа ввиде функции clean
        TestElement(OneToOneField=StepElement, r_n='test_content')
            Тоже что и TextElement но содержит вопрос по тексту
        TestOption(fk=TestElement, r_n='options)
            содержит флаг правильности ответа и ответ
        UserStepProgress(fk1=User, r_n=step_progress fk2=Step, r_n=user_progress)
            pass
''' 

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

        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_course_step_order')
        ]

    def __str__(self):
        return f'Заголовок: {self.course.title} - Шаг {self.order}: {self.title}'

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

        constraints = [
            models.UniqueConstraint(fields=['step', 'order'], name='unique_step_element_order')
        ]        

    def __str__(self):
        return f'Заголовок: {self.step.title} Номер: {self.order} Тип: [{self.get_step_element_type_display()}]'        

class TextElement(models.Model):
    step_element = models.OneToOneField(StepElement, on_delete=models.CASCADE, related_name='text_content')
    body = models.TextField(help_text='Текст статьи')

    def clean(self):
        # Защита: контент TEXT не должен быть привязан к элементу типа TEST
        if self.step_element.step_element_type != 'TEXT':
            raise ValidationError("Родительский элемент должен иметь тип 'TEXT'.")    


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

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Имя юзера: {self.username}'

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

    def save(self, *args, **kwargs):
        # Автоматически ставим дату, только если шаг пройден и дата еще не установлена
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)


