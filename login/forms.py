from django import forms
from django.contrib.auth.models import User

from login.models import JobSeekerProfile, EmployerProfile, Advertise

# Register forms -------------------------------------------------------------------------------------------------------

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

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
        fields = ('bio', )


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


# Other forms ----------------------------------------------------------------------------------------------------------

# class AdvertiseForm(forms.ModelForm):
#     class Meta:
#         model = Advertise
#         fields = ('title', 'type', 'category')

    # type = forms.ModelChoiceField


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = JobSeekerProfile
#         fields = ('image',)
