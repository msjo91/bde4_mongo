from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=20)
    gender = forms.ChoiceField(
        choices=User.CHOICES_GENDER,
        widget=forms.RadioSelect(),
    )

    def clean_username(self):
        """username field 검증 로직"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists!')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password2)
        if password1 != password2:
            raise forms.ValidationError('password1 and password2 not equal!')
        return password2

    def create_user(self):
        email = self.cleaned_data['email']
        password2 = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        gender = self.cleaned_data['gender']

        user = User.objects.create_user(
            email=email,
            password=password2,
            nickname=nickname
        )
        user.gender = gender
        user.save()
        return user


class SignupModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
            'gender',
        )


class ChangeProfileImageModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'profile_photo',
        )
