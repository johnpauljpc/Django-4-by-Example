
from django.contrib import admin
from django.urls import path,include
from blog import urls as blog_urls

urlpatterns = [
    path("blog/", include(blog_urls, namespace="blog")),
    path('admin/', admin.site.urls),

]
