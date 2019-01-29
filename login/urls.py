from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_account_job_seeker/', views.my_account_job_seeker, name="my_account_job_seeker")
]
