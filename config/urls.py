from django.contrib import admin
from django.urls import path
from intervals import views
from django_ask_sdk.skill_adapter import SkillAdapter

interval_training = SkillAdapter.as_view(
    skill=views.skill)

urlpatterns = [
    path('/', interval_training, name='index'),
    path('admin/', admin.site.urls),
]