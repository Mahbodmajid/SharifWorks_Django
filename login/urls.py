from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my-account-job-seeker/', views.my_account_job_seeker, name="my-account-job-seeker"),
    path('my-account-employer/', views.my_account_job_seeker, name="my-account-employer")
]
