
from django.contrib import admin
from django.urls import path,include
from blog import urls as blog_urls
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSiteMap

sitemaps = {
    "posts":PostSiteMap,
}

urlpatterns = [
    path("blog/", include(blog_urls, namespace="blog")),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
name='django.contrib.sitemaps.views.sitemap')
    # path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap')

]
