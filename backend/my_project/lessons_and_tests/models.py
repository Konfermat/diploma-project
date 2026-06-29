from django.db import models
from django.contrib.auth.models import AbstractUser

# null=True, blank=True # для чисел
# blank=True # для текста 

# --- БЛОК ЮЗЕРА ---
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# --- БЛОК УРОКА ---
class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
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

    def __str__(self):
        return f"{self.lesson.title} -> {self.title}"


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

    def __str__(self):
        part_title = self.lesson_part.title if self.lesson_part else "Нет части"
        return f"Текст ({self.order}) в {part_title}"


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

    def __str__(self):
        return f"Тест ({self.order}): {self.question[:30]}..."


class TestOption(models.Model):
    option = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавлено чтоб у всех было

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Ответ ({self.order}) для теста ID {self.option.id}"


# --- ИСТОРИЯ ОТВЕТОВ СТУДЕНТОВ ---
class UserTestAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_answers')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(TestOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> Тест {self.test.id} ({'Верно' if self.is_correct else 'Неверно'})"

    