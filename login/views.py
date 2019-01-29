from django.contrib.auth import login
from django.shortcuts import render, redirect
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


def job_seeker_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user.profile.image = profile_form.cleaned_data['image']
            login(request, user)
            return redirect('home')
        else:
            return redirect('index')
    else:
        return redirect('index')


def employer_register(request):
    return render(request, 'index.html')


def job_seeker_login(request):
    return render(request, 'index.html')


def employer_login(request):
    return render(request, 'index.html')
