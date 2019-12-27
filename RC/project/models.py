from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    p1_name = models.CharField(max_length=100)
    p1_email = models.CharField(max_length=100)
    mob1 = models.CharField(max_length=10)
    p2_name = models.CharField(max_length=100, default="a", null=True)
    p2_email = models.CharField(max_length=100, default="a@a.com", null=True)
    mob2 = models.CharField(max_length=10, default="9999999999", null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    login_time = models.DateTimeField(max_length=100, null=True)
    logout_time = models.DateTimeField(max_length=100, null=True)
    score = models.IntegerField(default=0)
    incr = models.IntegerField(default=4)
    decr = models.IntegerField(default=0)
    curqno = models.IntegerField(default=-1)
    attempt_cntr = models.IntegerField(default=2)
    level = models.IntegerField(default=1)
    visited = models.CharField(max_length=100, default="")
    correct = models.IntegerField(default=0)
    attempted = models.IntegerField(default=0)
    att1 = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.user.username


class Questions(models.Model):
    question = models.TextField(max_length=500, default="")
    answer = models.IntegerField(default=0)
    level = models.IntegerField(default=2)

    def __str__(self):
        return self.question + '--' + str(self.level)


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Questions, on_delete=models.CASCADE)
    attempt1 = models.IntegerField(default=0)
    attempt2 = models.IntegerField(default=0)

    def __str__(self):
        return (self.user.username + ' - ' + self.ques.question)
