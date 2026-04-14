from django.db import models
from django.contrib.auth.models import AbstractUser

#  (OneToOneField), 

# one to many,
# models.ForeignKey(Name, on_delete=CASADE) # Удаление вместе с потомством
# models.ForeignKey(Name, on_delete=PROTECT) # Удаление только если никто не привязан
# models.ForeignKey(Name, on_delete=SET_NULL, null=True) # Установит пустое значение
##########################################################################################

# https://docs.djangoproject.com/en/6.0/topics/db/examples/many_to_many/
# and many to many (ManyToManyField).

class User(AbstractUser):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name     

class Difficulty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

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
        return self.name

class Question(models.Model):
    #optional many to one (Test)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    def __str__(self):
        return self.name  

class Option(models.Model):
    #many to one (Question)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.name    

class Answer(models.Model):
    # many to one(Option)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    def __str__(self):
        return self.name    

class Attempt(models.Model):
    # many to one (User)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # many to one (Answer)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name    

# TODO ЗАКОНЧИ ЛОГИКУ
# НИЖЕ ИСПРАВЛЕНЫЫЙ ПРИМЕР ОТ ГУГЛА

'''
class Attempt(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE) # Нужно знать, какой тест проходим
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Попытка {self.user.name} - {self.test.name}"

class Answer(models.Model):
    # Теперь много ответов могут ссылаться на одну попытку
    attempt = models.ForeignKey('Attempt', on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Ответ на вопрос: {self.option.question.description[:20]}"

'''



