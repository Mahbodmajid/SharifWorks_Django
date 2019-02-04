from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # POST REQUESTS:
    path('jobseeker/', views.job_seeker_register, name="job-seeker-register"),
    path('employer/', views.employer_register, name="employer-register"),
    path('login/', views.login_view, name="login"),

    path('home/', views.home, name="home"),
    path('edit-resume/', views.edit_resume, name="edit-resume"),
    path('profile/', views.resume_page, name="resume-page"),
    path('add-job/', views.add_job, name="add-job"),
    path('logout/', views.logout_view, name="logout"),

    path('browse-jobs/', views.browse_jobs, name="browse-jobs"),
]
