from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def job_seeker_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a job seeker,
    redirects to the log-in page if necessary.
    '''

    # TODO login_url : doesn't redirect correctly
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_jobseeker,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def employer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is an employer,
    redirects to the log-in page if necessary.
    '''

    # TODO login_url : doesn't redirect correctly
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_employer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

