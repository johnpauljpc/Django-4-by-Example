from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = "blog"

urlpatterns = [
    path('', view=views.post_list, name="post-list"),
    path("tag/<slug:tag_slug>/", views.post_list, name = "post_list_by_tag" ),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name="post-detail"),
    path("post-share/<post_id>/", view=views.post_share, name="post-share"),
    path("comment/<int:post_id>/", view=views.CommentView, name="post_comment"),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', view=views.searchView, name="post_search"),
]