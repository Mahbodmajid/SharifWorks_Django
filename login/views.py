from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from login.forms import RegisterForm, JobSeekerProfileForm, UpdateUserForm, EmployerRegisterForm, AdvertiseForm, \
    CommentForm, AdvertiseSearchForm
from login.models import JobSeekerProfile, EmployerProfile, Advertise, Skill, JobReq
from django.contrib.auth import get_user_model
from login.decorators import employer_required, job_seeker_required

User = get_user_model()


# from login.models import Advertise


def index(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        # print(data)
        uid_list.append(data.get('_auth_user_id', None))

    online_users = len(uid_list)

    # users = User.objects.all()
    # online_users = []
    # for user in users:
    #     if user.is_authenticated:
    #         online_users.append(user)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'index.html', {'online_users': online_users})


# register


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
            return redirect('home')
        else:
            context = {'errors': {
                'user': user_form.errors,
            }}
            return render(request, 'my-account-job-seeker.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            register_form = RegisterForm
            context = {'register_form': register_form}
            return render(request, 'my-account-job-seeker.html', context)


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
            return redirect('home')
        else:
            context = {'errors': {
                'user': user_form.errors,
                'profile': profile_form.errors
            }}
            return render(request, 'my-account-employer.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            register_form = RegisterForm
            employer_register_form = EmployerRegisterForm
            context = {'register_form': register_form,
                       'employer_register_form': employer_register_form}
            return render(request, 'my-account-employer.html', context)


# login


def job_seeker_login(request):
    if request.method == 'POST':
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
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return redirect('job-seeker-register')


def employer_login(request):
    if request.method == 'POST':
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
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return redirect('employer-register')


def user_posts(request):
    user = request.user  # khode user TODO: change
    posts = Advertise.objects.filter(employer=user)
    return render(request, 'index.html', posts)


@login_required(login_url='login')
@job_seeker_required
def edit_resume(request):
    context = {}
    if request.method == 'POST':
        print(request.POST.get('bio'))
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=request.user)
        print(user_form)
        print(profile_form)
        print("-----------------------")
        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.save()
            profile.job_seeker_profile.save()
            ## TODO skills and cv are not working correctly
            context['success'] = 'تغییرات شما با موفقیت ذخیره‌شد.'
        else:
            context['errors'] = {
                'user': user_form.errors,
                'profile': profile_form.errors
            }
    user_form = UpdateUserForm
    profile_form = JobSeekerProfileForm
    job_seeker = JobSeekerProfile.objects.get(user_id=request.user.id)
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['job_seeker'] = job_seeker
    return render(request, 'edit-resume.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


@login_required(login_url='login')
@employer_required
def add_job(request):
    if request.method == 'POST':
        add_job_form = AdvertiseForm(request.POST)
        print("Add Advertisement Request")
        if add_job_form.is_valid():
            employer = EmployerProfile.objects.get(user_id=request.user.id)
            advertise = add_job_form.save(commit=False)
            advertise.employer_id = employer.id
            advertise.save()
            print("title: ", advertise.title)
            print("type: ", advertise.type)
            print("category: ", advertise.category)
            print("deadline: ", advertise.deadline)
            print("description: ", advertise.description)
            print("address: ", advertise.address)
            context = {
                'success': 'آگهی با موفقیت ثبت شد.'
            }
            return render(request, "job-form.html", context)
        context = {
            'errors': add_job_form.errors,
            'before': {
                'title': request.POST.get("title"),
                'type': request.POST.get("type"),
                'category': request.POST.get("category"),
                'deadline': request.POST.get("deadline"),
                'description': request.POST.get("description"),
                'address': request.POST.get("address")
            }
        }
        print("Form Not Valid", add_job_form.errors)
        return render(request, "job-form.html", context)
    elif request.method == 'GET':
        advertise_form = AdvertiseForm
        return render(request, 'job-form.html', {'advertise_form': advertise_form})


@login_required(login_url='login')
def home(request, response=None):
    if request.user.is_jobseeker is True:
        return render(request, 'job-seeker-home.html', response)
    else:
        return render(request, 'employer-home.html', response)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if len(users) == 0:
            response = {'error': "چنین کاربری وجود ندارد."}
            return render(request, 'login.html', response)
        elif not users[0].check_password(password):
            response = {'error': "رمز عبور صحیح نیست."}
            return render(request, 'login.html', response)
        user = users[0]
        login(request, user)
        response = {'success': "شما با موفقیت وارد شدید."}
        return home(request, response)
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'login.html')


def browse_jobs(request):
    city = request.GET.get('city')
    skills = request.GET.getlist('skills')
    print("Ad Search. city: ", city, "skills: ", skills)
    search_form = AdvertiseSearchForm
    related_advs = []
    for adv in Advertise.objects.all():  # TODO: search based on skills
        if adv.city == city:
            related_advs.append(adv)

    context = {'search_form': search_form, 'advs': related_advs}
    return render(request, 'browse-jobs.html', context)


def employer_profile(request):
    if request.method == "GET":
        id = request.body  # TODO
        employer = EmployerProfile.objects.get(id)
        return render(request, 'employer-profile.html', {'employer': employer})
    elif request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # comment.job_seeker =
            # comment.employer =
            # return redirect('home')


@login_required(login_url='login')
def resume_page(request):
    user_form = UpdateUserForm
    profile_form = JobSeekerProfileForm
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'job-seeker-profile.html', context)


@require_GET
@login_required(login_url='login')
def profile_view(request):
    user_id = request.GET.get("user_id", "")
    if user_id == "":
        user_id = request.user.id
    query_user = User.objects.filter(id=user_id)
    if len(query_user) == 0:
        context = {'error': 'کاربر مورد نظر یافت نشد.'}
        return render(request, 'error_page.html', context)
    else:
        profile_contents = None
        if query_user[0].is_jobseeker:
            profile_contents = JobSeekerProfile.objects.get(user_id=user_id)
            context = {'profile': profile_contents}
            return render(request, 'job-seeker-profile.html', context)

        elif query_user[0].is_employer:
            profile_contents = EmployerProfile.objects.get(user_id=user_id)
            context = {'profile': profile_contents}
            return render(request, 'employer-profile.html', context)


@require_POST
@login_required(login_url='login')
@job_seeker_required
def comment_view(request):
    user_id = request.GET.get("user_id")
    employers = EmployerProfile.objects.filter(user_id=user_id)
    if len(employers) == 0:
        context = {'error': 'کارفرمای مورد نظر یافت نشد.'}
        return render(request, 'error_page.html', context)
    employer = employers[0]
    profile_contents = EmployerProfile.objects.get(user_id=user_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.employer = employer
        comment.job_seeker = JobSeekerProfile.objects.get(user_id=request.user.id)
        print(comment)
        comment.save()
        context = {
            'profile': profile_contents,
            'success': 'نظر با موفقیت ثبت شد.'
        }
        return render(request, "employer-profile.html", context)
    else:
        context = {'profile': profile_contents,
                   'errors': comment_form.errors,
                   'before': {
                       'rate': request.POST.get('rate'),
                       'description': request.POST.get('description')
                   }}
        return render(request, 'employer-profile.html', context)


@login_required(login_url='login')
def job_view(request):
    if request.method == "GET":
        adv_id = request.GET.get('advertise_id', '')
        job_reqs = JobReq.objects.filter(advertise_id=adv_id, job_seeker__user_id=request.user.id)
        state = 0
        job_req = None
        if len(job_reqs) == 1:
            job_req = job_reqs[0]
            state = job_req.state
        elif len(job_reqs) > 1:
            state = -1  # invalid

        if adv_id == '' or not str.isdigit(adv_id):
            context = {'error': 'آگهی مورد نظر یافت نشد.'}
            return render(request, 'error_page.html', context)

        query_advertise = Advertise.objects.filter(id=adv_id)
        if len(query_advertise) == 0:
            context = {'error': 'آگهی مورد نظر یافت نشد.'}
            return render(request, 'error_page.html', context)
        advertise = query_advertise[0]

        return render(request, 'job-page.html', {'advertise': advertise, 'state': state})
    else:
        context = {'error': 'آگهی مورد نظر یافت نشد.'}
        return render(request, 'error_page.html', context)


@login_required(login_url='login')
def job_requests_view(request):
    if request.method == "POST":
        adv_id = request.POST.get('advertiese_id')
        if adv_id == '':
            return HttpResponse("failure", content_type="text/plain")
        query_advertise = Advertise.objects.filter(id=adv_id)
        if len(query_advertise) == 0:
            return HttpResponse("failure", content_type="text/plain")

        jobseekeer = JobSeekerProfile.objects.get(user_id=request.user.id)
        js_id = jobseekeer.id

        query_jobreq = JobReq.objects.filter(advertise_id=adv_id, job_seeker_id=js_id)
        if len(query_jobreq) > 0:
            return HttpResponse("failure", content_type="text/plain")

        JobReq.objects.create(state=1, advertise_id=adv_id, job_seeker_id=js_id)
        return HttpResponse("success", content_type="text/plain")
    elif request.method == "GET":
        user_id = request.GET.get("user_id", "")
        return render(request, 'job-page.html', {'employer': EmployerProfile.objects.get(user_id)})


