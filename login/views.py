from django.contrib.auth import login
from django.shortcuts import render, redirect
from login.forms import RegisterForm, JobSeekerRegisterForm, EmployerRegisterForm, LoginForm


def index(request):
    return render(request, 'index.html')


def my_account_job_seeker(request):
    login_form = LoginForm
    register_form = RegisterForm
    context = {'login_form': login_form, 'register_form': register_form}
    return render(request, 'my-account-job-seeker.html', context)


def my_account_employer(request):
    login_form = LoginForm
    register_form = RegisterForm
    employer_register_form = EmployerRegisterForm
    context = {'login_form': login_form, 'register_form': register_form,
               'employer_register_form': employer_register_form}
    return render(request, 'my-account-employer.html', context)


def job_seeker_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        # profile_form = JobSeekerRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            # user.jobseekerprofile.bio = profile_form.cleaned_data['bio']
            # user.jobseekerprofile.cv = profile_form.cleaned_data['cv']
            login(request, user)
            return redirect('job-seeker-home')  # TODO
        else:
            return redirect('my-account-job-seeker')  # TODO
    else:
        return redirect('my-account-job-seeker')  # TODO


def employer_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = EmployerRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user.employerprofile.company_name = profile_form.cleaned_data['company_name']
            user.employerprofile.company_type = profile_form.cleaned_data['company_type']
            user.employerprofile.company_disc = profile_form.cleaned_data['company_disc']
            login(request, user)
            return redirect('home')  # TODO
        else:
            return redirect('index')  # TODO
    else:
        return redirect('index')  # TODO


def job_seeker_login(request):
    return render(request, 'index.html')


def employer_login(request):
    return render(request, 'index.html')


def job_seeker_home(request):
    return render(request, 'job-seeker-home.html')


def employer_home(request):
    return render(request, 'employer-home.html')


def edit_resume(request):
    return render(request, 'edit-resume.html')


def resume_page(request):
    return render(request, 'resume-page.html')


def add_job(request):
    return render(request, 'add-job.html')


def logout(request):
    logout(request)
    return redirect('index')

