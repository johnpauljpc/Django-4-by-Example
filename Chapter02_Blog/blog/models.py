from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    STATUS = (("draft", "Draft"), ("published", "Published"))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date = 'publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default="draft")

    objects = models.Manager()  # default manager
    published = PublishedManager()  # Custum manager

    class Meta:
        ordering = ["-publish"]
        indexes = (models.Index(fields=["-publish"]),)

    def get_absolute_url(self):
        return reverse(
            "blog:post-detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "post": self.slug,
            },
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE) #by Default -> related_name = comment_set
    # user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "comments")
    name = models.CharField(max_length = 40)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)


    class Meta:
        ordering = ['created']

        indexes = (models.Index(fields=['created']),)

    def __str__(self):
        return f"comment by {self.name} on {self.post}"