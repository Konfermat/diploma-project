from django.db import models
from django.contrib.auth.models import AbstractUser

#  (OneToOneField), 
# one to many (ForeignKey) 
# and many to many (ManyToManyField).

class User(AbstractUser):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

class Test(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    #many to many (User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty  (Choices: Easy, Medium, Hard)
    is_published 

class Question(models.Model):
    #optional many to one (Test)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

class Option(models.Model):
    #many to one (Question)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    is_correct = models.BooleanField(default=False)

class Result(models.Model):
    # many to one (User)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # many to one (Test)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class UserAttempt(models.Model):
    # many to one (User)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # many to one (Test)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()

class UserAnswer(models.Model):
    # many to one (Question)
    attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE)
    # many to one (Question)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # many to one (Option)
    option = 

# ОШИБКИ ИСПРАВЬ    

class Topic(models.Model):
    pass
