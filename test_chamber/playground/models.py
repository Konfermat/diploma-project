from django.db import models

#  (OneToOneField), 
# one to many (ForeignKey) 
# and many to many (ManyToManyField).

class User(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class Test(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    #many to many (User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    #optional many to one (Test)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

class Option(models.Model):
    #many to one (Question)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    is_correct = models.BooleanField(default=False)

class Result(models.Model):
    # many to one (User)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # many to one (Test)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class UserAttemt(models.Model):
    # many to one (User)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # many to one (Test)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()

class UserAnswer(models.Model):
    # many to one (Question)
    attempt_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # many to one (Question)
    question_id = 
    # many to one (Option)
    option_id = 

# ОШИБКИ ИСПРАВЬ    