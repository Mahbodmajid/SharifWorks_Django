from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def my_account_job_seeker(request):
    login_form = JSLoginForm
    register_form = JSRegisterForm
    context = {'login_form': login_form, 'register_form': register_form}
    return render(request, 'my-account-job-seeker.html', context)

