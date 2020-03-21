from datetime import datetime, timedelta
import random
import re
from sqlite3 import IntegrityError

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate

from .models import Questions, Profile, Response

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def signup(request):
    try:
        if request.method == "POST":
            user = User.objects.create_user(username=request.POST.get('uname'), password=request.POST.get('pass'))
            p1_name = request.POST.get('p1_name')
            p1_email = request.POST.get('p1_email')
            mob1 = request.POST.get('mob1')
            p2_name = request.POST.get('p2_name')
            p2_email = request.POST.get('p2_mail')
            mob2 = request.POST.get('mob2')
            level = request.POST.get('level')
            level = int(level)
            userprofile = Profile(p1_name=p1_name, p1_email=p1_email, mob1=mob1, p2_name=p2_name, p2_email=p2_email,
                                  mob2=mob2, user=user, level=level)

            if re.search(regex, p1_email):
                auth.login(request, user)
                userprofile.login_time = datetime.now(login(request, user))
                userprofile.logout_time = userprofile.login_time + timedelta(seconds=1740)
                userprofile.save()
                return render(request, 'RCIns.html')
            else:
                return render(request, 'signup.html', {'error': "Email not valid"})
        else:
            return render(request, 'signup.html')
    except IntegrityError:
        return render(request, 'signup.html')



@login_required
def rand_que(request):
    try:
        profile = Profile.objects.get(user=request.user)
        cur_time = datetime.now()
        time_remain = (profile.logout_time.hour * 60 * 60) + (
                profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                              cur_time.minute * 60) - cur_time.second
        while True:
            try:
                if profile.attempted < 60:
                    if profile.level == 0:
                        qno = random.randint(1, 59)
                        for i in profile.visited.split(','):
                            if i != str(qno):
                                continue
                            else:
                                return redirect(reverse('index2'))
                                break
                        profile.visited = profile.visited + ',' + str(qno)
                        questions = Questions.objects.get(pk=qno, level=profile.level)
                        profile.curqno = qno
                        profile.save()
                        return redirect(reverse('first'))
                    if profile.level == 1:
                        qno = random.randint(60, 121)
                        for i in profile.visited.split(','):
                            if i != str(qno):
                                continue
                            else:
                                return redirect(reverse('index2'))
                                break
                        profile.visited = profile.visited + ',' + str(qno)
                        questions = Questions.objects.get(pk=qno, level=profile.level)
                        profile.curqno = qno
                        profile.save()
                        return redirect(reverse('first'))
                else:
                    return redirect(reverse('login_logout'))
            except Questions.DoesNotExist:
                continue
    except:
        return redirect(reverse('signup'))


@login_required
def marking_scheme(request, qno):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        if profile.attempt_cntr != 1:
            answer = Questions.objects.get(pk=qno)
            profile.curqno = qno
            ans1 = request.POST.get('attempt1')
            profile.att1 = ans1
            profile.save()
            if ans1:
                response = Response.objects.create(user=request.user, ques=answer, attempt1=int(ans1))
                response.save()
                if answer.answer == int(ans1):
                    profile.score = profile.score + profile.incr
                    profile.correct = profile.correct + 1
                    profile.attempted = profile.attempted + 1
                    profile.save()
                    return redirect(reverse('index2'))
                else:
                    profile.incr = 2
                    profile.decr = -1
                    profile.attempt_cntr = 1
                    profile.save()
                    profile = Profile.objects.get(user=request.user)
                    cur_time = datetime.now()
                    cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
                    logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                                      profile.logout_time.second
                    time_remain = logout_time_sec - cur_time
                    qno = profile.curqno
                    questions = Questions.objects.get(pk=qno)
                    context = {'profile': profile, 'question': questions, 'your_time': time_remain,
                               'answer': int(ans1)}
                    return render(request, 'Codingpage.html', context)

            else:
                questions = Questions.objects.get(pk=profile.curqno)
                cur_time = datetime.now()
                cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
                logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                                  profile.logout_time.second
                time_remain = logout_time_sec - cur_time
                context = {'profile': profile, 'question': questions, 'your_time': time_remain}
                return render(request, 'Codingpage.html', context)

        elif profile.attempt_cntr == 1:
            ans2 = request.POST.get('attempt2')
            answer = Questions.objects.get(pk=profile.curqno)
            if ans2:
                if answer.answer == int(ans2):
                    profile.score = profile.score + profile.incr
                    profile.correct = profile.correct + 1
                    profile.save()
                else:
                    profile.score = profile.score + profile.decr
                    profile.save()

                profile.attempt_cntr = 2
                profile.attempted = profile.attempted + 1
                profile.incr = 4
                profile.decr = 0
                profile.save()
                response = Response.objects.create(user=request.user, ques=answer, attempt2=int(ans2))
                response.save()
                return redirect(reverse('index2'))
            else:
                cur_time = datetime.now()
                time_remain = (profile.logout_time.hour * 60 * 60) + (
                        profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                                      cur_time.minute * 60) - cur_time.second
                questions = Questions.objects.get(pk=profile.curqno)
                context = {'profile': profile, 'question': questions, 'your_time': time_remain,
                           'answer': int(profile.att1)}
                return render(request, 'Codingpage.html', context)

    else:
        profile = request.user.Profile
        questions = Questions.objects.get(pk=profile.curqno, level=profile.level)
        cur_time = datetime.now()
        time_remain = (profile.logout_time.hour * 60 * 60) + (
                profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                              cur_time.minute * 60) - cur_time.second
        profile.save()
        context = {'profile': profile, 'question': questions, 'your_time': time_remain}
        return render(request, 'Codingpage.html', context)


def login_logout1(request, qno):
    try:
        profile = request.user.Profile
        profile.logout_time = datetime.now()
        profile.save()
        auth.logout(request)
        context = {'login': profile.login_time, 'profile': profile, 'logout': profile.logout_time,
                   'score': profile.score}
        return render(request, 'Result_page.html', context)
    except:
        return redirect(reverse('signup'))


def login_logout(request):
    try:
        profile = request.user.Profile
        profile.logout_time = datetime.now()
        profile.save()
        auth.logout(request)
        context = {'login': profile.login_time, 'profile': profile, 'logout': profile.logout_time,
                   'score': profile.score}
        return render(request, 'Result_page.html', context)
    except:
        return redirect(reverse('signup'))


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@login_required
def instruction(request):
    userprofile = Profile.objects.get(user=request.user)
    userprofile.login_time = datetime.now()
    userprofile.logout_time = userprofile.login_time + timedelta(minutes=28)
    userprofile.save()
    return redirect(reverse('index2'))


def function(request, garbage):
    try:
        profile = request.user.Profile
        questions = Questions.objects.get(pk=profile.curqno, level=profile.level)
        cur_time = datetime.now()
        time_remain = (profile.logout_time.hour * 60 * 60) + (
                profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                              cur_time.minute * 60) - cur_time.second
        profile.save()
        context = {'login': profile.login_time, 'profile': profile, 'logout': profile.logout_time,
                   'score': profile.score}
        return render(request, 'Codingpage.html', context)
    except:
        return render(request, 'signup.html')


@login_required
def first(request):
    if request.method == "POST":
        return redirect(reverse('index2'))
    else:
        profile = request.user.Profile
        if profile.curqno == -1:
            profile.save()
            return redirect(reverse('index2'))
        else:
            profile.save()
        questions = Questions.objects.get(pk=profile.curqno, level=profile.level)
        cur_time = datetime.now()
        time_remain = (profile.logout_time.hour * 60 * 60) + (
                profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                              cur_time.minute * 60) - cur_time.second
        context = {'profile': profile, 'question': questions, 'your_time': time_remain}
        return render(request, 'Codingpage.html', context)


def emergency(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('superpass')
        extratime = request.POST.get('time')

        if not password1 == "TPPN2019":
            return render(request, 'emergency.html', {'error': "Super Password is wrong"})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                profile = Profile.objects.get(user=request.user)
                profile.logout_time = profile.logout_time + timedelta(seconds=int(extratime))
                profile.save()
                questions = Questions.objects.get(pk=profile.curqno, level=profile.level)
                cur_time = datetime.now()
                time_remain = (profile.logout_time.hour * 60 * 60) + (
                        profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                                      cur_time.minute * 60) - cur_time.second
                context = {'profile': profile, 'question': questions, 'your_time': time_remain}
                return render(request, 'Codingpage.html', context)
        else:
            return render(request, 'emergency.html')
    else:
        return render(request, 'emergency.html')
