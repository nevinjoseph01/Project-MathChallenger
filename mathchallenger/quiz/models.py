
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    SELECTION = (("teacher","Teacher"),("student","Student"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=8, choices=SELECTION)

    def __str__(self):
        return self.user.username + '\' profile'


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    difficulty = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username + '\' scores'



class QuesModel(models.Model):
    SELECTION = (
        ('beginner', 'Beginner'),
        ('medium', 'Medium'),
        ('advanced', 'Advanced'),
        ('human_calculator', 'Human Calculator'),
    )
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    difficulty = models.CharField(max_length=20, choices=SELECTION, default='beginner')
    def __str__(self):
        return self.question


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    average = models.IntegerField()
    entries = models.IntegerField()
    difficulty = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username + '\' stats'


