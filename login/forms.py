from django import forms
from django.contrib.auth.models import User

from login.models import JobSeekerProfile


class JobSeekerLoginForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('email', 'password')

    email = forms.EmailInput(label='ایمیل')
    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)


class JobSeekerRegisterForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار گذرواژه", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(JobSeekerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'readonly': 'readonly'}

    def clean(self):
        super(JobSeekerRegisterForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('رمزها همخوانی ندارند.')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('image',)
