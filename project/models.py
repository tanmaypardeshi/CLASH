from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator


class Profile(models.Model):
    timer = models.TimeField(null=True)
    p1_name = models.CharField(max_length=100)
    p1_email = models.CharField(max_length=100)
    mob1 = models.CharField(max_length=12)
    p2_name = models.CharField(max_length=100, default="a")
    p2_email = models.CharField(max_length=100, default="a@a.com")
    mob2 = models.CharField(max_length=12, default="9999999999")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    login_time = models.DateTimeField(null=True, max_length=100)
    logout_time = models.DateTimeField(max_length=100, null=True)
    score = models.IntegerField(default=0)
    incr = models.IntegerField(default=4)
    decr = models.IntegerField(default=2)
    visited = models.CharField(max_length=100, default="")
    buff1 = models.IntegerField(default=0)
    buff2 = models.IntegerField(default=0)
    buff3 = models.IntegerField(default=0)
    buff_cntr = models.IntegerField(default=0)
    level = models.IntegerField(default=2)
    list_cntr = models.IntegerField(default=0)
    endian_counter = models.IntegerField(default=0)
    lifeline1 = models.IntegerField(default=0)
    stack = models.IntegerField(default=6)
    buff_que_added = models.IntegerField(default=0)
    bon_que_timer = models.TimeField(null=True)
    bon_score = models.IntegerField(default=32)
    correct = models.IntegerField(default=0)
    life_counter = models.IntegerField(default=0)
    bon_intime = models.TimeField(null=True)
    bon_outtime = models.TimeField(null=True)
    curqno = models.IntegerField(default=-1)
    after_bonus = models.IntegerField(default=0)
    attempted = models.IntegerField(default=0)
    after_buff = models.IntegerField(default=0)
    bon_flag = models.IntegerField(default=0)
    bon_ans = models.CharField(default="", max_length=500)

    def __str__(self):
        return self.user.username


class Questions(models.Model):
    question = models.TextField(max_length=5000, default="")
    option1 = models.CharField(max_length=100, default="")
    option2 = models.CharField(max_length=100, default="")
    option3 = models.CharField(max_length=100, default="")
    option4 = models.CharField(max_length=100, default="")
    answer = models.CharField(max_length=100, default="")
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.question


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Questions, on_delete=models.CASCADE)
    resp = models.CharField(max_length=100, default="", null=True)
