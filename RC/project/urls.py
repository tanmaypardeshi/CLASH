from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('first/', never_cache(views.first), name='first'),
    path('RCinstr/', views.instruction, name='instruction'),
    path('question/', never_cache(views.rand_que), name='index2'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('answer/<int:qno>/', never_cache(views.marking_scheme), name='index3'),
    path('first/question/logout/', views.login_logout, name='login_logout'),
    path('answer/<int:qno>/question/logout/', views.login_logout1, name='login_logout1'),
    path('first/logout/', views.login_logout),
    path('question/logout/', views.login_logout),
    path('answer/logout/', views.login_logout),
    path('logout/', views.login_logout),
    path('emergency/', views.emergency, name='emergency'),
    url(r'^(?P<garbage>.*)/$', views.function, name='function'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
