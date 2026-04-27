from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'имя юзера: {self.username}'

class Topic(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'название темы: {self.name}'     

class Difficulty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'сложность: {self.name}'

class Test(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    #many to many (User)
    created_by = models.ManyToManyField('User')
    created_at = models.DateTimeField(auto_now_add=True)
    # many to optional one optional (Difficulty)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    # many to one optional (Topic)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'название теста: {self.name}'

class Question(models.Model):
    # оne to many (Test)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions')
    description = models.TextField(max_length=1000)
    def __str__(self):
        return f'вопрос: {self.description}'

class Option(models.Model):
    #many to one (Question)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return f'вариант ответа: {self.description}'   

class Attempt(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'имя пользователя: {self.user.username}, название теста: {self.test.name}'

class UserAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    # many to one (Option) UserAnswer may have many options
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    def __str__(self):
        return f'попытка: {self.attempt}, вопрос: {self.question},  выбранные варианты: {self.selected_option}'


  






