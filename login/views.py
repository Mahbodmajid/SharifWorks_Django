from django.shortcuts import render
from login.forms import JobSeekerLoginForm, JobSeekerRegisterForm, EmployerLoginForm, EmployerRegisterForm


def index(request):
    return render(request, 'index.html')


def my_account_job_seeker(request):
    login_form = JobSeekerLoginForm
    register_form = JobSeekerRegisterForm
    context = {'login_form': login_form, 'register_form': register_form}
    return render(request, 'my-account-job-seeker.html', context)


def my_account_employer(request):
    login_form = EmployerLoginForm
    register_form = EmployerRegisterForm
    context = {'login_form': login_form, 'register_form': register_form}
    return render(request, 'my-account-employer.html', context)

