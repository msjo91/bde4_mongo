"""
Integrate custom user model (MyUser) to admin page.
생성한 커스텀 유저 모델(MyUser)을 admin 페이지에 반영한다.
Referred to Django Documentation v1.11
공식문서 참조
https://docs.djangoproject.com/en/1.11/topics/auth/customizing/
"""
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    Modelform for creating users including required fields and repeated passwords.
    필수 필드와 비밀번호를 이용해 이용자를 생성하는 모델폼.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        """
        Check if the repeated passwords match.
        입력한 두 비밀번호가 같은지 확인한다.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("재입력한 비밀번호가 다릅니다.")
        return password2

    def save(self, commit=True):
        """
        Save given password hashed.
        비밀번호를 해쉬로 변환해 저장한다.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Modelform for updating user.
    Display password hashed.
    이용자 업데이트를 위한 모델폼.
    비밀번호는 해쉬화해서 보여준다.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'nickname', 'is_active', 'is_admin')

    def clean_password(self):
        """
        Return initial value regardless of user input.
        이용자의 입력과 관계없이 비밀번호 초기값을 불러온다.
        """
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    """
    Form to add and update user instances.
    이용자 인스턴스의 추가, 수정을 위한 폼.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    # Override default UserAdmin (as BaseUserAdmin) with fields in MyUser model.
    # 기본 UserAdmin(BaseUserAdmin으로 개명)을 MyUser 모델의 필드로 덮어쓴다.
    list_display = ('email', 'nickname', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'profile_photo')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    # Override get_fieldsets when creating user.
    # 이용자 생성시 get_fieldsets를 덮어쓴다.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'profile_photo')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group, )
