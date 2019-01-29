from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my-account-job-seeker/', views.my_account_job_seeker, name="my-account-job-seeker"),
    path('my-account-employer/', views.my_account_job_seeker, name="my-account-employer"),
    path('job-seeker-registration', views.job_seeker_register, name="job-seeker-register"),
    path('employer-registration', views.employer_register, name="employer-register"),
    path('job-seeker-login', views.job_seeker_login, name="job-seeker-login"),
    path('employer-login', views.employer_login, name="employer-login"),
]
