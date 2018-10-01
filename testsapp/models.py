from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class TestGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateTimeField(default=datetime.now)
    test_group = models.ManyToManyField(TestGroup)


class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Answer(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)


class UserResult(models.Model):
    date_passing = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    number_correct_answers = models.IntegerField()

