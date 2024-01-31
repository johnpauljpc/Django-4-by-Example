from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = "published")
    

class Post(models.Model):
    STATUS = (('draft', 'Draft'),
              ('published', 'Published'))
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "blog_posts")
    content = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 20, choices = STATUS, default = "draft")

    objects = models.Manager()  #default manager
    published = PublishedManager() #Custum manager
    
    class Meta:
        ordering = ['-publish']
        indexes = models.Index(fields=['-publish']),
   


    def __str__(self):
        return self.title
    

