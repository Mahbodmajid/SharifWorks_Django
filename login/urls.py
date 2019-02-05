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
    path('profile/', views.profile_view, name="profile"),
    path('job/', views.job_view, name="job"),
    path('comment/', views.comment_view, name="comment"),
    path('add-job/', views.add_job, name="add-job"),
    path('logout/', views.logout_view, name="logout"),
    path('browse-jobs/', views.browse_jobs, name="browse-jobs"),
    path('request-job/', views.job_requests_view, name="request-job"),
    path('manage-jobs/', views.employer_requests_view, name="manage-jobs"),
    path('resume/', views.download_resume_view, name="resume")
]
