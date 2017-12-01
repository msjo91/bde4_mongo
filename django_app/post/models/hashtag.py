from django.db import models

from .post import Post

__all__ = (
    'HashTag',
)


class HashTag(models.Model):
    """
    HashTag model
    """
    name = models.CharField(max_length=64, unique=True)
    post = models.ManyToManyField(Post)

    def __unicode__(self):
        return self.name
