from django.contrib.auth.models import User
from django.db import models

    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [("teacher", "Teacher")]


class Quizzes(models.Model):
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [("student", "Student")]


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    associated_quizzes = models.ManyToManyField(Quizzes)

    def __str__(self):
        return self.question_text



class AnswerChoice(models.Model):
    choice_text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, related_name="choices",on_delete=models.CASCADE)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
