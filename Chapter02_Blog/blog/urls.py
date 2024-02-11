from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', view=views.post_list, name="post-list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name="post-detail"),
    path("post-share/<post_id>/", view=views.post_share, name="post-share"),
    path("comment/<int:post_id>/", view=views.CommentView, name="post_comment"),
]