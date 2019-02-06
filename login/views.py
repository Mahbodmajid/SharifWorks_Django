from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.models import Avg, Case, Count, When
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
            if not user_form.cleaned_data['password'] == user_form.cleaned_data['password2']:
                return render(request, 'my-account-employer.html', {'errors': {'user': 'رمزها برابر نیستند.'}})
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
            if not user_form.cleaned_data['password'] == user_form.cleaned_data['password2']:
                return render(request, 'my-account-employer.html', {'errors': {'user': 'رمزها برابر نیستند.'}})
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
        print(request.POST.getlist('skills'))
        print("BIO", request.POST.get('bio'))

        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.save()
            profile.job_seeker_profile.bio = profile_form.cleaned_data['bio']
            profile.job_seeker_profile.title = profile_form.cleaned_data['title']
            profile.job_seeker_profile.address = profile_form.cleaned_data['address']
            if profile_form.cleaned_data['cv'] is None:
                profile.job_seeker_profile.cv = request.user.job_seeker_profile.cv
            else:
                profile.job_seeker_profile.cv = profile_form.cleaned_data['cv']
            profile.job_seeker_profile.save()

            profile.job_seeker_profile.skills.clear()

            new_skills = request.POST.getlist('skills')
            for new_skill in new_skills:
                if len(Skill.objects.filter(name=new_skill)) == 0:
                    new_skill_object = Skill.objects.create(name=new_skill)
                else:
                    new_skill_object = Skill.objects.get(name=new_skill)
                profile.job_seeker_profile.skills.add(new_skill_object)

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
    context['all_skills'] = Skill.objects.all()
    context['your_skills'] = request.user.job_seeker_profile.skills.all()
    return render(request, 'edit-resume.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


@login_required(login_url='login')
@employer_required
def add_job(request):
    advertise_form = AdvertiseForm
    context = {'advertise_form': advertise_form}
    if request.method == 'POST':
        add_job_form = AdvertiseForm(request.POST)
        print("Add Advertisement Request")
        if add_job_form.is_valid():
            employer = EmployerProfile.objects.get(user_id=request.user.id)
            advertise = add_job_form.save(commit=False)
            advertise.employer_id = employer.id
            advertise.save()
            new_skills = request.POST.getlist('skills')
            print(new_skills)
            for new_skill in new_skills:
                if len(Skill.objects.filter(name=new_skill)) == 0:
                    new_skill_object = Skill.objects.create(name=new_skill)
                else:
                    new_skill_object = Skill.objects.get(name=new_skill)
                advertise.skills.add(new_skill_object)

            context['success'] = 'آگهی با موفقیت ثبت شد.'
            context['all_skills'] = Skill.objects.all()
            return render(request, "job-form.html", context)
        else:
            context['all_skills'] = Skill.objects.all()
            context['errors'] = add_job_form.errors
            context['before'] = {
                'title': request.POST.get("title"),
                'city': request.POST.get("city"),
                'type': request.POST.get("type"),
                'category': request.POST.get("category"),
                'deadline': request.POST.get("deadline"),
                'description': request.POST.get("description"),
                'address': request.POST.get("address"),
                'skills': request.POST.getlist("skills")
            }
            return render(request, "job-form.html", context)
    elif request.method == 'GET':
        context['all_skills'] = Skill.objects.all()
        return render(request, 'job-form.html', context)


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


@login_required(login_url='login')
@job_seeker_required()
@require_GET
def browse_jobs(request):
    search_form = AdvertiseSearchForm
    city = request.GET.getlist('city')
    skills = request.GET.getlist('skills')
    print("Ad Search. city: ", city, "skills: ", skills)
    related_advs = []
    for adv in Advertise.objects.all():
        if adv.city in city or len(city) == 0:
            adv_skills = [str(skill.id) for skill in adv.skills.all()]

            if len(set.intersection(set(skills), set(adv_skills))) > 0 or len(skills) == 0:
                adv.score = len(set.intersection(set(skills), set(adv_skills)))
                related_advs.append(adv)

    def sort_function(e):
        return e.score

    related_advs.sort(key=sort_function)

    no_result = False
    if len(related_advs) == 0:
        no_result = True
    if (city == []) and (skills == []):
        no_result = False

    context = {'search_form': search_form,
               'advs': related_advs,
               'no_results': no_result,
               'before': {
                   'city': city,
                   'skills': [int(skill) for skill in skills]
               }}
    return render(request, 'browse-jobs.html', context)


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
            rate_double = profile_contents.comment_set.aggregate(Avg('rate'))['rate__avg']
            rate = None
            if rate_double is not None:
                rate = round(rate_double)
            count = profile_contents.comment_set.count() - \
                    profile_contents.comment_set.filter(rate=None).count()
            context = {'profile': profile_contents, 'rate': rate, 'count': count}
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
        rate = round(profile_contents.comment_set.aggregate(Avg('rate'))['rate__avg'])
        count = profile_contents.comment_set.count() - \
                profile_contents.comment_set.filter(rate=None).count()
        context = {
            'profile': profile_contents,
            'success': 'نظر با موفقیت ثبت شد.',
            'rate': rate,
            'count': count}
        return render(request, "employer-profile.html", context)
    else:
        rate = round(profile_contents.comment_set.aggregate(Avg('rate'))['rate__avg'])
        count = profile_contents.comment_set.count() - \
                profile_contents.comment_set.filter(rate=None).count()
        context = {'profile': profile_contents,
                   'errors': comment_form.errors,
                   'before': {
                       'rate': request.POST.get('rate'),
                       'description': request.POST.get('description'),
                   },
                   'rate': rate,
                   'count': count}

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
        if request.user.is_jobseeker:
            adv_id = request.POST.get('advertiese_id')
            if adv_id == '':
                return HttpResponse("failure", content_type="text/plain")
            query_advertise = Advertise.objects.filter(id=adv_id)
            if len(query_advertise) == 0:
                return HttpResponse("failure", content_type="text/plain")

            jobseeker = JobSeekerProfile.objects.get(user_id=request.user.id)
            js_id = jobseeker.id

            query_jobreq = JobReq.objects.filter(advertise_id=adv_id, job_seeker_id=js_id)
            if len(query_jobreq) > 0:
                return HttpResponse("failure", content_type="text/plain")

            JobReq.objects.create(state=1, advertise_id=adv_id, job_seeker_id=js_id)
            return HttpResponse("success", content_type="text/plain")
    elif request.method == "GET":
        user_id = request.GET.get("user_id", "")
        return render(request, 'job-page.html', {'employer': EmployerProfile.objects.get(user_id)})


@login_required(login_url='login')
def employer_requests_view(request):
    if request.method == "GET":
        employer = EmployerProfile.objects.get(user_id=request.user.id)
        job_reqs = JobReq.objects.filter(advertise__employer_id=employer.id, state=1)
        print(job_reqs)
        return render(request, 'manage-jobs.html', {'job_reqs': job_reqs})
    elif request.method == "POST":
        print("POST req:")
        print(request)
        jobreq_id = request.POST.get('jobreq_id')
        confirmed = request.POST.get('confirmed')
        if jobreq_id == '':
            return HttpResponse("failure", content_type="text/plain")
        query_jobreq = JobReq.objects.filter(id=jobreq_id)
        if len(query_jobreq) == 0:
            return HttpResponse("failure", content_type="text/plain")

        if len(query_jobreq) > 1:
            return HttpResponse("failure", content_type="text/plain")

        job_req = JobReq.objects.filter(id=jobreq_id)
        if confirmed == '1':
            job_req.update(state=2)
        elif confirmed == '0':
            job_req.update(state=3)
        return HttpResponse("success", content_type="text/plain")


@login_required()
def download_resume_view(request):
    if request.method == "GET":
        job_seeker_id = request.GET.get("job_seeker_id", "")
        if job_seeker_id == "":
            job_seeker_id = request.user.job_seeker_profile.id
        has_right = False
        if request.user.is_employer:
            has_right = True
        elif request.user.is_jobseeker:
            print(job_seeker_id, request.user.job_seeker_profile.id)
            job_seeker_id = int(job_seeker_id)
            if request.user.job_seeker_profile.id == job_seeker_id:
                has_right = True
        if has_right:
            candidates = JobSeekerProfile.objects.filter(id=job_seeker_id)
            if len(candidates) > 0:
                resume_file = candidates[0].cv
                if resume_file == "" or resume_file is None:
                    return render(request, 'error_page.html', {
                        'error': 'این کارجو رزومه ندارد.'
                    })
                response = HttpResponse(resume_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
                return response
            else:
                return render(request, 'error_page.html', {
                    'error': 'کارجوی مورد نظر وجود ندارد.'
                })
        else:
            return render(request, 'error_page.html', {'error': 'شما مجاز به دیدن این صفحه نیستید.'})


@login_required()
def result_view(request):
    if request.method == "GET":
        if request.user.is_jobseeker:
            print("JS")
            job_reqs = JobReq.objects.filter(job_seeker_id=request.user.job_seeker_profile.id)
            return render(request, 'job-seeker-results.html', {'job_reqs': job_reqs})
        else:
            return None