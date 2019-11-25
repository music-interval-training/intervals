from django.contrib import admin
from django.urls import path
from intervals import views
from django_ask_sdk.skill_adapter import SkillAdapter

interval_training = SkillAdapter.as_view(
    skill=views.skill)
# ToDo Make a default index view. Dont want root url to hit alexa skill
# create homepage view 
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('intervals/progress_details', views.progress_details, name='progress_details'), 
    path('alexa', interval_training, name='alexa'),
    path('admin/', admin.site.urls),
    path('intervals/progress_details', views.progress_details, name='progress_details'),
]