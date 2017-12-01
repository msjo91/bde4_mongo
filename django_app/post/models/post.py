"""
1. Post모델 구현 (like_users빼고)
    photo에 ImageField사용
    pip install Pillow

2. PostLike모델 구현 (중간자 모델로 사용)
3. Post모델의 like_users필드 구현
4. Comment모델 구현
"""
from django.conf import settings
from django.db import models

__all__ = (
    'Post',
    'PostLike',
)


class PostManager(models.Manager):
    def visible(self):
        return super().get_queryset().filter(is_visible=True)


class PostUserVisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Post(models.Model):
    """
    1. Post모델에서 content 필드를 없애고 Db migration
    2. post_add view의 동작을 변경 (입력받은 content는 새 Comment객체를 생성하도록)
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(
        upload_to='post', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_post_set',
    )
    is_visible = models.BooleanField(default=True)

    # Default 모델 매니저 교체
    objects = PostManager()
    # 커스텀 모델 매니저 추가
    visible = PostUserVisibleManager()

    # Post.objects.visible()
    # Post.visible.all()

    def __str__(self):
        return 'Post[{}]'.format(self.id)

    class Meta:
        ordering = ('-id',)

    def toggle_like(self, user):
        # PostLike 중간자모델에서 인자로 전달된 Post, MyUser객체를 가진 row를 조회
        # pl_list = PostLike.objects.filter(post=self, user=user)
        pl_list = self.postlike_set.filter(user=user)

        # # 현재 인자로 전달된 user가 해당 Post(self)를 좋아요 한 적이 있는지 검사
        # # if self.like_users.filter(id=user.id).exists():
        # if pl_list.exists():
        #     # 만약에 이미 좋아요를 했을 경우 해당 내역을 삭제
        #     # 중간자 모델을 사용하기 때문에 self.like_users.remove()대신 아래 메서드를 사용
        #     # PostLike.objects.filter(post=self, user=user).delete()
        #     pl_list.delete()
        # else:
        #     # 아직 내역이 없을 경우 생성해준다
        #     # 중간자 모델을 사용하기 때문에 self.like_users.create()대신 PostLike중간자 모델 매니저를 사용한다
        #     PostLike.objects.create(post=self, user=user)

        # 파이썬 삼항연산자 (위의 if/else문을 한 줄로)
        # [True일 경우 실행할 구문] if 조건문 else [False일 경우 실행할 구문]
        # pl_list.delete() if pl_list.exists() else PostLike.objects.create(post=self, user=user)
        return self.postlike_set.create(user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        # 자신에게 연결된 Comment객체의 역참조 매니저(comment_set)로부터
        # create메서드를 이용해 Comment객체를 생성
        return self.comment_set.create(
            author=user,
            content=content
        )

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

    def __str__(self):
        return 'Post[{}]\'s Like[{}], User[{}]'.format(
            self.post_id,
            self.id,
            self.user_id,
        )
