from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/jobseeker/', views.my_account_job_seeker, name="my-account-job-seeker"),
    path('accounts/employer/', views.my_account_employer, name="my-account-employer"),
    path('accounts/jobseeker/register/', views.job_seeker_register, name="job-seeker-register"),
    path('accounts/employer/register/', views.employer_register, name="employer-register"),
    path('accounts/jobseeker/login/', views.job_seeker_login, name="job-seeker-login"),
    path('accounts/employer/login/', views.employer_login, name="employer-login"),
    path('jobseeker/home/', views.job_seeker_home, name="job-seeker-home"),
    path('jobseeker/edit/', views.edit_resume, name="edit-resume"),
    path('jobseeker/profile/', views.resume_page, name="resume-page"),
    path('employer/home/', views.employer_home, name="employer-home"),
    path('employer/new-job/', views.add_job, name="add-job"),
    path('accounts/logout/', views.logout, name="logout")
]
