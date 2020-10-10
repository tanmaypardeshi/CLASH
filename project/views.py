import random
import re
import time
from _datetime import datetime, timedelta
from threading import Timer

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .models import Questions, Profile, Response

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['uname'])
            return render(request, 'signup.html', {'error': "Username Has Already Been Taken"})
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['uname'], password=request.POST['pass'])
            p1_name = request.POST['p1_name']
            p1_email = request.POST['p1_email']
            mob1 = request.POST['mob1']
            p2_name = request.POST['p2_name']
            p2_email = request.POST['p2_email']
            mob2 = request.POST['mob2']
            level = request.POST['year']

            userprofile = Profile(p1_name=p1_name, p1_email=p1_email, mob1=mob1, p2_name=p2_name, p2_email=p2_email,
                                  mob2=mob2, user=user, level=level)

        if re.search(regex, p1_email):
            auth.login(request, user)
            userprofile.login_time = datetime.now()
            userprofile.logout_time = userprofile.login_time + timedelta(minutes=30)
            userprofile.save()

            return redirect(reverse('inst'))
        else:
            return render(request, 'signup.html', {'error': "Email not valid"})
    else:
        return render(request, 'signup.html')


@login_required
def instructions(request):
    if request.method == "GET":
        userprofile = Profile.objects.get(user=request.user)

        context = {'profile': userprofile}

        return render(request, 'ins.html', context)
    else:
        userprofile = Profile.objects.get(user=request.user)
        userprofile.login_time = datetime.now()
        userprofile.logout_time = userprofile.login_time + timedelta(minutes=28)
        if userprofile.level == 3:
            userprofile.level = request.POST.get('choose')
        userprofile.save()

        return redirect(reverse('post', kwargs={'qno': 0}))


@login_required
def rand_que(request, _id):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        if profile.curqno == _id:
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            print(logout_time_sec)
            time_remain = logout_time_sec - cur_time
            print(time_remain)
            try:

                questions = Questions.objects.get(pk=_id, level=profile.level)
                profile.visited = profile.visited + ',' + str(_id)
                profile.curqno = _id
                if profile.lifeline1:
                    if profile.endian_counter == 4:
                        profile.incr = 16
                        profile.decr = 16
                    elif profile.endian_counter == 3:
                        profile.incr = 8
                        profile.decr = 8
                    elif profile.endian_counter == 2:
                        profile.incr = 4
                        profile.decr = 4
                    elif profile.endian_counter == 1:
                        profile.incr = 2
                        profile.decr = 2
                    else:
                        profile.lifeline1 = 0

                context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                           'buff2': profile.buff2, 'profile': profile,
                           'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                           'buff_que_added': profile.buff_que_added,
                           'your_time': time_remain, 'lifeline1': profile.lifeline1,
                           'lifeline2': profile.life_counter}
                profile.save()
                return render(request, 'Question.html', context)
            except Questions.DoesNotExist:
                print("hi")
                profile.curqno = -1
                return redirect(reverse('post', kwargs={'qno': 0}))
            while True:
                pass
        else:
            questions = Questions.objects.get(pk=profile.curqno)
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                       'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain, 'message': 'abe select toh kar', 'lifeline1': profile.lifeline1,
                       'lifeline2': profile.life_counter}
            return render(request, 'Question.html', context)


@login_required
def marking_scheme(request, qno):
    profile = request.user.Profile
    if profile.curqno != -1 and qno != 0:
        answer = Questions.objects.get(pk=qno)
        ans = request.POST.get('options')
        if ans:
            if answer.answer == ans:
                profile.score = profile.score + profile.incr
                profile.incr = 4
                profile.decr = 2
                if profile.lifeline1 == 0:
                    if profile.stack < 6:
                        profile.stack = profile.stack + 1
                else:
                    profile.endian_counter = profile.endian_counter - 1
                profile.correct = profile.correct + 1
            else:
                profile.score = profile.score - profile.decr
                profile.incr = 4
                profile.decr = 2
                if profile.lifeline1 == 0:
                    if profile.stack != 0:
                        profile.stack = profile.stack - 1
                else:
                    profile.endian_counter = profile.endian_counter - 1
            profile.attempted = profile.attempted + 1
            response = Response.objects.create(user=request.user, ques=answer, resp=ans)
            response.save()
            profile.save()
        else:
            questions = Questions.objects.get(pk=qno)
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                       'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain, 'message': 'abe select toh kar', 'lifeline1': profile.lifeline1,
                       'lifeline2': profile.life_counter}
            return render(request, 'Question.html', context)

    if profile.level == 2:
        _id = random.randint(1439, 1556)
    elif profile.level == 1:
        _id = random.randint(978, 1438)
    else:
        _id = random.randint(14, 977)
    for i in profile.visited.split(','):
        if i != str(_id):
            continue
        else:
            profile.curqno = -1
            profile.save()
            return redirect(reverse('post', kwargs={'qno': 0}))

    profile.life_counter = 0
    profile.curqno = _id
    profile.save()
    return HttpResponseRedirect(reverse('question', kwargs={'_id': _id}))


def login_logout(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile.score = profile.score - profile.buff_que_added * 2
        if profile.bon_flag == 1:
            if profile.bon_ans is None:
                profile.score = profile.score - 8
        profile.logout_time = datetime.now()
        profile.save()
        context = {'login': profile.login_time, 'profile': profile, 'logout': profile.logout_time,
                   'score': profile.score}
        auth.logout(request)
        return render(request, 'Result_page.html', context)
    except:
        return redirect(reverse('signup'))


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@login_required()
def buffer(request, qno):
    try:
        profile = request.user.Profile
        if profile.buff1 == 0:
            profile.buff1 = qno
            print(profile.buff1)
            profile.buff_cntr = profile.buff_cntr + 1
            profile.buff_que_added = profile.buff_que_added + 1
            profile.curqno = -1
            profile.save()
            messages.info(request, 'Added successfully to buffer!')
            return redirect(reverse('post', kwargs={'qno': 0}))
        elif profile.buff2 == 0:
            profile.buff2 = qno
            profile.buff_cntr = profile.buff_cntr + 1
            profile.buff_que_added = profile.buff_que_added + 1
            profile.curqno = -1
            profile.save()
            messages.info(request, 'Added successfully to buffer!')
            return redirect(reverse('post', kwargs={'qno': 0}))
        elif profile.buff3 == 0:
            profile.buff3 = qno
            profile.buff_cntr = profile.buff_cntr + 1
            profile.buff_que_added = profile.buff_que_added + 1
            profile.curqno = -1
            profile.save()
            messages.info(request, 'Added successfully to buffer!')
            return redirect(reverse('post', kwargs={'qno': 0}))
        elif profile.buff_cntr > 2:
            full_buff = {'isfull': (profile.buff_cntr > 2)}
            return JsonResponse(full_buff)
    except AnonymousUser:
        return render(request, 'signup.html')


@login_required
def buff_quest(request):
    profile = request.user.Profile
    if 'bffr1' in request.POST:
        if profile.buff1 != 0:
            questions = Questions.objects.get(pk=profile.buff1, level=profile.level)
            qno = profile.buff1
            profile.buff1 = 0
            profile.buff_cntr = 0
            profile.buff_que_added = profile.buff_que_added - 1
            profile.life_counter = 2
            profile.curqno = qno
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            profile.save()
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                       'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain}
            print(profile.score)

            print("This is my score")
            return redirect(reverse('question', kwargs={'_id': qno}))
        else:
            return JsonResponse({'buff1': profile.buff1, 'buff2': profile.buff2, 'buff3': profile.buff3,
                                 'full_buff': profile.buff_cntr})
    elif 'bffr2' in request.POST:
        if profile.buff2 != 0:
            questions = Questions.objects.get(pk=profile.buff2, level=profile.level)
            qno = profile.buff2
            profile.buff2 = 0
            profile.buff_cntr = 1
            profile.buff_que_added = profile.buff_que_added - 1
            profile.life_counter = 2
            profile.curqno = qno
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            profile.save()
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                       'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain}
            print(profile.score)

            print("This is my score")
            return redirect(reverse('question', kwargs={'_id': qno}))
        else:
            return messages.info(request, "no buffer")
    elif 'bffr3' in request.POST:
        if profile.buff3 != 0:
            questions = Questions.objects.get(pk=profile.buff3, level=profile.level)
            qno = profile.buff3
            profile.buff3 = 0
            profile.buff_cntr = 2
            profile.life_counter = 2
            profile.buff_que_added = profile.buff_que_added - 1
            profile.curqno = qno
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            profile.save()
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                       'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain}
            print(profile.score)

            print("This is my score")
            return redirect(reverse('question', kwargs={'_id': qno}))


@login_required
def endian_activated(request):
    profile = Profile.objects.get(user=request.user)
    profile.lifeline1 = 1
    profile.stack = 0
    profile.endian_counter = 4
    profile.life_counter = 1
    profile.incr = 16
    profile.decr = 16
    profile.save()
    cur_time = datetime.now()
    cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
    logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                      profile.logout_time.second
    time_remain = logout_time_sec - cur_time
    questions = Questions.objects.get(pk=profile.curqno)
    context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
               'buff2': profile.buff2, 'profile': profile,
               'buff3': profile.buff3, 'full_buff': profile.buff_cntr, 'buff_que_added': profile.buff_que_added,
               'your_time': time_remain, 'lifeline1': profile.lifeline1, 'lifeline2': profile.life_counter}
    return render(request, 'Question.html', context)


def endian_marking(request, qno):
    try:
        profile = Profile.objects.get(user=request.user)
        answer = Questions.objects.get(pk=qno)
        ans = request.POST.get('options')
        if ans:
            if profile.lifeline1 == 1:
                if profile.endian_counter == 1:
                    profile.life_counter = 0
                profile.lifeline1 = 0
                profile.stack = 0
                if profile.endian_counter == 0:
                    profile.incr = 4
                    profile.decr = 2
            if answer.answer == ans:
                profile.score = profile.score + profile.incr
                profile.correct = profile.correct + 1
            else:
                profile.score = profile.score - profile.decr
            profile.attempted = profile.attempted + 1
            response = Response.objects.create(user=request.user, ques=answer, resp=ans)
            response.save()
            profile.save()
            return redirect(reverse('question'))
        else:
            questions = Questions.objects.get(pk=profile.curqno)
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                              profile.logout_time.second
            time_remain = logout_time_sec - cur_time
            context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                       'buff2': profile.buff2, 'profile': profile,
                       'buff3': profile.buff3, 'full_buff': profile.buff_cntr, 'buff_que_added': profile.buff_que_added,
                       'your_time': time_remain}
            return render(request, 'Question.html', context)
    except AnonymousUser:
        return render(request, 'signup.html')


@login_required
def bonus_ques(request):
    profile = Profile.objects.get(user=request.user)
    if profile.bon_flag != 1:
        junior_ques_py = [1685, 1686, 1687, 1688, 1689]
        bonus_senior = [1682, 1683, 1684]

        if profile.level == 2:
            _id = junior_ques_py[random.randint(0, 4)]
        else:
            _id = bonus_senior[random.randint(0, 2)]

        question = Questions.objects.get(id=_id)
        profile.curqno = _id
        bon_intime = datetime.now()
        if profile.after_bonus != 1:
            profile.bon_intime = datetime.now()
            profile.bon_outtime = profile.bon_intime + timedelta(seconds=130)
            now = (profile.bon_outtime.hour * 60 * 60) + (
                    profile.bon_outtime.minute * 60) + profile.bon_outtime.second - \
                  (bon_intime.hour * 60 * 60) - (bon_intime.minute * 60) - bon_intime.second
        else:
            now = (profile.bon_outtime.hour * 60 * 60) + (
                    profile.bon_outtime.minute * 60) + profile.bon_outtime.second - \
                  (bon_intime.hour * 60 * 60) - (bon_intime.minute * 60) - bon_intime.second

        profile.after_bonus = 1
        profile.bon_flag = 1
        profile.save()
        context = {'question': question, 'score': profile.score, 'now': now, 'profile': profile}
        return render(request, 'bonus.html', context)
    else:
        questions = Questions.objects.get(id=profile.curqno)
        cur_time = datetime.now()
        cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
        bon_out_time_sec = (profile.bon_outtime.hour * 60 * 60) + (profile.bon_outtime.minute * 60) + \
                           profile.bon_outtime.second
        now = bon_out_time_sec - cur_time
        context = {'question': questions, 'score': profile.score, 'now': now, 'profile': profile}
        return render(request, 'bonus.html', context)


@login_required
def bonus_ques_ans(request, bqno):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        answer = Questions.objects.get(pk=bqno)
        bon_outtime = datetime.now()
        time_gap = (bon_outtime.hour * 60 * 60) + (bon_outtime.minute * 60) + bon_outtime.second - \
                   (profile.bon_intime.hour * 60 * 60) - (profile.bon_intime.minute * 60) - profile.bon_intime.second
        profile.bon_ans = request.POST.get('option')
        if profile.bon_ans:
            if answer.answer == profile.bon_ans:
                if time_gap < 10:
                    profile.score = profile.score + 32
                elif 10 < time_gap <= 20:
                    profile.score = profile.score + 16
                elif 20 < time_gap <= 30:
                    profile.score = profile.score + 8
                elif 30 < time_gap <= 40:
                    profile.score = profile.score + 4
                elif 40 < time_gap <= 50:
                    profile.score = profile.score + 2
                elif 50 < time_gap <= 60:
                    profile.score = profile.score + 1
                else:
                    profile.score = profile.score + 0
            else:
                if 70 < time_gap <= 80:
                    profile.score = profile.score - 1
                elif 80 < time_gap <= 90:
                    profile.score = profile.score - 2
                elif 90 < time_gap <= 100:
                    profile.score = profile.score - 4
                elif 100 < time_gap <= 110:
                    profile.score = profile.score - 8
                elif 110 < time_gap <= 120:
                    profile.score = profile.score - 16
                elif 120 < time_gap <= 130:
                    profile.score = profile.score - 32
                else:
                    profile.score = profile.score - 0
            profile.save()
            return redirect(reverse('login_logout'))
        else:
            questions = Questions.objects.get(id=bqno)
            cur_time = datetime.now()
            cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
            bon_out_time_sec = (profile.bon_outtime.hour * 60 * 60) + (profile.bon_outtime.minute * 60) + \
                               profile.bon_outtime.second
            now = bon_out_time_sec - cur_time
            context = {'question': questions, 'score': profile.score, 'now': now, 'profile': profile}
            return render(request, 'bonus.html', context)
    else:
        return redirect(reverse('login_logout'))


def questions_post(request):
    try:
        profile = Profile.objects.get(user=request.user)
        _id = random.randint(1, 22)
        return HttpResponseRedirect(reverse('question', kwargs={'_id': _id}))
    except:
        return render(request, 'signup.html')


def function(request, garbage):
    try:
        profile = Profile.objects.get(user=request.user)
        questions = Questions.objects.get(pk=profile.curqno)
        cur_time = datetime.now()
        cur_time = (cur_time.hour * 60 * 60) + (cur_time.minute * 60) + cur_time.second
        logout_time_sec = (profile.logout_time.hour * 60 * 60) + (profile.logout_time.minute * 60) + \
                          profile.logout_time.second
        time_remain = logout_time_sec - cur_time
        context = {'question': questions, 'score': profile.score, 'buff1': profile.buff1,
                   'buff2': profile.buff2, 'profile': profile,
                   'buff3': profile.buff3, 'full_buff': profile.buff_cntr,
                   'buff_que_added': profile.buff_que_added,
                   'your_time': time_remain, 'message': 'abe select toh kar', 'lifeline1': profile.lifeline1,
                   'lifeline2': profile.life_counter}
        return render(request, 'Question.html', context)
    except:
        return redirect(reverse('signup'))


def emergency(request):
    if request.method == 'POST':
        superpass = "TPPN2019"
        uname = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('superpass')
        extratime = request.POST.get('time')
        print(extratime)
        if authenticate(username=uname, password=password):
            if password1 == superpass:
                user = User.objects.get(username=uname)
                auth.login(request, user)
                profile = Profile.objects.get(user=user)
                profile.logout_time = profile.logout_time + timedelta(seconds=int(extratime))
                profile.save()
                return redirect(reverse('question', kwargs={'_id': profile.curqno}))
            else:
                context = {'error': "Passwords don't match"}
                return render(request, 'emergency.html', context)
        else:
            context = {'error': "Username does not exist"}
            return render(request, 'emergency.html', context)
    else:
        return render(request, 'emergency.html')
