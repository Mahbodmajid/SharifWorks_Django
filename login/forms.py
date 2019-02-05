from django import forms
from django.contrib.auth.models import User

from login.models import JobSeekerProfile, EmployerProfile, Advertise, Choices, Skill, Comment, JobReq
from django.contrib.auth import get_user_model

User = get_user_model()


# Register forms -------------------------------------------------------------------------------------------------------


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password2')

    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار گذرواژه", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'readonly': 'readonly'}

    def clean(self):
        super(RegisterForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('رمزها همخوانی ندارند.')


class JobSeekerRegisterForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        # fields = ('bio', 'homepage', 'cv')
        fields = ('bio',)


class EmployerRegisterForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ('company_name', 'company_disc', 'company_type')


# Login forms ----------------------------------------------------------------------------------------------------------


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)


# Update Profile forms ------------------------------------------------------------------------------------------------

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('bio', 'homepage', 'cv', 'skills')

    skills = forms.ModelChoiceField(queryset=Skill.objects.all(), widget=forms.SelectMultiple)


# Advertise forms -----------------------------------------------------------------------------------------------------


class AdvertiseForm(forms.ModelForm):
    class Meta:
        model = Advertise
        fields = ('title', 'type', 'category', 'deadline', 'description', 'city', 'address')

    title = forms.CharField(error_messages={'required': 'عنوان کار را وارد کنید.'})
    city = forms.CharField(error_messages={'required': 'شهر کار را وارد کنید.'})
    type = forms.ChoiceField(choices=Choices.JOBTYPES,
                             error_messages={'required': 'نوع کار را وارد کنید.',
                                             'invalid_choice': 'نوع کار معتبر نیست'})
    category = forms.ChoiceField(choices=Choices.JOBCATS,
                                 error_messages={'required': 'دسته‌بندی کار را وارد کنید.',
                                                 'invalid_choice': 'دسته‌بندی کار معتبر نیست'}
                                 )
    deadline = forms.DateField(error_messages={'required': 'تاریخ اتمام کار را وارد کنید.',
                                               'invalid': 'تاریخ اتمام کار معتبر نیست'})


# class JobReqForm(forms.ModelForm):
#     class Meta:
#         model = JobReq

class AdvertiseSearchForm(forms.ModelForm):
    class Meta:
        model = Advertise
        fields = ('city', 'skills')

    skills = forms.ModelChoiceField(queryset=Skill.objects.all(), widget=forms.SelectMultiple)
    city = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description', 'rate',)

#     TODO: COMMENT FORM VALIDATION
