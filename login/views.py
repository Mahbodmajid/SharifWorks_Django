from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from login.forms import RegisterForm, JobSeekerProfileForm, UpdateUserForm, EmployerRegisterForm, LoginForm, AdvertiseForm
from login.models import JobSeekerProfile, EmployerProfile, Advertise, Skill
from django.contrib.auth import get_user_model
from login.decorators import employer_required, job_seeker_required

User = get_user_model()


# from login.models import Advertise


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
            user.is_jobseeker = True
            user.save()
            job_seeker = JobSeekerProfile.objects.create(user=user)
            # user.jobseekerprofile.bio = profile_form.cleaned_data['bio']
            # user.jobseekerprofile.cv = profile_form.cleaned_data['cv']
            login(request, user)
            return redirect('job-seeker-home')
        else:
            return redirect('my-account-job-seeker')
    else:
        return redirect('my-account-job-seeker')


def employer_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = EmployerRegisterForm(request.POST)
        print("Employer Register Request")
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_employer = True
            user.save()
            employer = EmployerProfile.objects.create(user=user,
                                                      company_name=profile_form.cleaned_data['company_name'],
                                                      company_disc=profile_form.cleaned_data['company_disc'],
                                                      company_type=profile_form.cleaned_data['company_type'])
            user.employer_profile.company_name = profile_form.cleaned_data['company_name']
            user.employer_profile.company_type = profile_form.cleaned_data['company_type']
            user.employer_profile.company_disc = profile_form.cleaned_data['company_disc']
            login(request, user)
            print("Employer Signed In:")
            print("Username: ", user.username)
            print("Password: ", user.password)
            print("company_name: ", user.employer_profile.company_name)
            print("company_type: ", user.employer_profile.company_type)
            print("company_disc: ", user.employer_profile.company_disc)
            return redirect('employer-home')
        else:
            return redirect('my-account-employer')
    else:
        return redirect('my-account-employer')


def job_seeker_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    users = User.objects.filter(username=username, is_jobseeker=True)
    if len(users) == 0:
        response = {'error': "چنین کاربری وجود ندارد.", 'tab': "1"}
        return render(request, 'my-account-job-seeker.html', response)
    elif not users[0].check_password(password):
        response = {'error': "رمز عبور صحیح نیست.", 'tab': "1"}
        return render(request, 'my-account-job-seeker.html', response)
    login(request, users[0])
    response = {'success': "شما با موفقیت وارد شدید."}
    return render(request, 'job-seeker-home.html', response)


def employer_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    users = User.objects.filter(username=username, is_employer=True)
    if len(users) == 0:
        response = {'error': "چنین کاربری وجود ندارد.", 'tab': "1"}
        return render(request, 'my-account-employer.html', response)
    elif not users[0].check_password(password):
        response = {'error': "رمز عبور صحیح نیست.", 'tab': "1"}
        return render(request, 'my-account-employer.html', response)
    login(request, users[0])
    response = {'success': "شما با موفقیت وارد شدید."}
    return render(request, 'employer-home.html', response)


def user_posts(request):
    user = request.user  # khode user TODO: change
    posts = Advertise.objects.filter(employer=user)
    return render(request, 'index.html', posts)


@login_required(login_url='my-account-job-seeker')
@job_seeker_required
def job_seeker_home(request):
    return render(request, 'job-seeker-home.html')


@login_required(login_url='my-account-employer')
@employer_required
def employer_home(request):
    return render(request, 'employer-home.html')


@login_required(login_url='my-account-job-seeker')
@job_seeker_required
def edit_resume(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.user)
        print(type(request.user))
        # user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=request.user.job_seeker_profile)
        if profile_form.is_valid():
                # and user_form.is_valid():
            # user = request.user  # user that is logged in
            # user_form.save()
            profile_form.save_m2m()
            return redirect('employer-home')
        else:
            # print(user_form.errors)
            print(profile_form.errors)
            return redirect('my-account-employer')
    else:
        user_form = UpdateUserForm
        profile_form = JobSeekerProfileForm
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'edit-resume.html', context)


@login_required(login_url='my-account-job-seeker')
@job_seeker_required
def resume_page(request):
    user_form = UpdateUserForm
    profile_form = JobSeekerProfileForm
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'resume-page.html', context)


@login_required(login_url='my-account-employer')
@employer_required
def job_form(request):
    advertise_form = AdvertiseForm
    return render(request, 'job-form.html', {'advertise_form': advertise_form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='my-account-employer')
@employer_required
def add_job(request):
    if request.method == 'POST':
        add_job_form = AdvertiseForm(request.POST)
        print("Add Advertisement Request")
        if add_job_form.is_valid():
            user = request.user
            advertise = add_job_form.save(commit=False)
            advertise.employer_id = user.id
            advertise.save()
            print("title: ", advertise.title)
            print("type: ", advertise.type)
            print("category: ", advertise.category)
            print("deadline: ", advertise.deadline)
            print("description: ", advertise.description)
            print("address: ", advertise.address)
            context = {
                'errors': {},
                'success': 'آگهی با موفقیت ثبت شد.'
            }
            return render(request, "employer-home.html", context)
        context = {
            'errors': add_job_form.errors,
            'success': {}
        }
        print("Form Not Valid", add_job_form.errors)
        return render(request, "job-form.html", context)
