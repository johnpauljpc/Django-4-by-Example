from ..models import Post, Comment
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()

@register.simple_tag
def total_post():
    posts = Post.published.all().count()
    return posts

@register.inclusion_tag('latest_posts.html')
def latest_posts(count=5):
    latest_posts = Post.published.all().order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_post(count=5):
    posts = Post.published.annotate(comments = Count('comment')).order_by('-comments','-publish')[:count]
    return posts


# Filters
@register.filter
def make_upper(text):
    return str(text).upper()

@register.filter(name="capitalize")
def Capitalize(text):
    return str(text).capitalize()

@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))