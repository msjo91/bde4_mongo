"""
Design user information and creation models.
이용자 정보 및 생성 모델 작성.
Referred to Django Documentation v1.11
공식문서 참조
https://docs.djangoproject.com/en/1.11/topics/auth/customizing/
"""

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        Create user using email, nickname and password.
        이메일, 닉네임, 비밀번호를 이용해 이용자를 생성한다.
        """
        if not email:
            raise ValueError('이메일 주소는 필수로 입력해야 합니다.')

        if not nickname:
            raise ValueError('닉네임은 필수로 입력해야 합니다.')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        """
        Create superuser using email, nickname and password.
        이메일, 닉네임, 비밀번호를 이용해 운영자를 생성한다.
        """
        user = self.create_user(
            email=email,
            nickname=nickname,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(PermissionsMixin, AbstractBaseUser):
    CHOICES_GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'No Answer')
    )

    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True,
    )

    nickname = models.CharField(
        verbose_name='nickname',
        max_length=30,
        unique=True,
    )

    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    profile_photo = models.ImageField(upload_to='post', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 팔로우 목록을 나타내는 필드 구현
    # 언제 팔로우를 했는지도 나타내도록 함 (중간자모델을 사용해야 함)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='follower_set',
        through='RelationShip',
    )

    # 메서드 추가
    # MyUser를 팔로우 (자신의 following목록에 추가)
    def follow(self, user):
        self.following_relations.create(
            to_user=user
        )

    def unfollow(self, user):
        self.following_relations.filter(
            to_user=user
        ).delete()

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        User has a specific permission.
        이용자는 특정 권한이 있다.
        """
        return True

    def has_module_perms(self, app_label):
        """
        User has permissions to view 'app_label'.
        이용자는 '앱 이름'을 볼 권한이 있다.
        """
        return True

    @property
    def is_staff(self):
        """
        All admins are staff.
        모든 관리자 계정은 운영자 권한을 갖는다.
        """
        return self.is_admin


class RelationShip(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='following_relations')
    to_user = models.ForeignKey(MyUser, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user',)
        )

    def __str__(self):
        return 'Relation from({}) to({})'.format(
            self.from_user.username,
            self.to_user.username,
        )
