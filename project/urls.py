from django.conf.urls import url
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('emergency/', views.emergency, name='emergency'),
    # re_path(r'/', views.function, name='func'),
    path('', views.signup, name='signup'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('instructions/', views.instructions, name='inst'),
    path('question-post/<int:qno>/', views.marking_scheme, name='post'),
    path('question/<int:_id>/', views.rand_que, name='question'),
    path('question/answer/answer/<int:qno>/', views.marking_scheme, name='index3'),
    path('answer/<int:qno>/', views.marking_scheme, name='index3'),
    path('answer/answer/<int:qno>/', views.marking_scheme),
    path('question/answer/<int:qno>/', views.marking_scheme, name='post1'),
    path('question/pushinbuffer/<int:qno>/', views.buffer, name='buffer'),
    path('question/activate/', views.endian_activated, name='endian'),
    path('question/lifeline/<int:qno>/', views.marking_scheme, name='indexx'),
    path('question/logout/', views.login_logout, name='login_logout'),
    path('question/buff/', views.buff_quest),
    path('question/buff/activate/', views.endian_activated),
    # path('question/buff/answer/<int:qno>/', views.marking_scheme),
    # path('question/logout/gotobonus/', views.bonus_ques, name='gotobonus'),
    # path('question/logout/gotobonus/bonusanswer/<int:bqno>/', views.bonus_ques_ans, name='bonus_ques_ans'),
    path('question/question/answer/<int:qno>/', views.marking_scheme),
    path('question/answer/activate/', views.endian_activated),
    path('pushinbuffer/<int:qno>/', views.buffer),
    path('question/answer/logout/', views.login_logout),
    path('logout/', views.login_logout),
    path('question/activate/logout/', views.login_logout),
    path('question/gotobonus/', views.bonus_ques, name='bonus'),
    path('question/gotobonus/logout/', views.login_logout),
    path('question/gotobonus/bonusanswer/<int:bqno>/', views.bonus_ques_ans, name='bon_ans'),
    path('question/gotobonus/bonusanswer/bonusanswer/<int:bqno>/', views.bonus_ques_ans),
    path('question/bonusanswer/<int:bqno>/', views.bonus_ques_ans),
    url(r'^(?P<garbage>.*)/$', views.function, name='func'),


]
