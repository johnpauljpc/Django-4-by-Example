from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Count
from django.contrib.postgres.search import (SearchVector, SearchQuery,
                                             SearchRank, TrigramSimilarity)

from .models import Post, Comment
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm, SearchForm


# print("--------------")
# tag = Tag.objects.get(id = 1)
# print(tag)
# posts = Post.published.filter(tags=tag)
# print("--------")
# print(posts)
# print(Tag.objects.all())
# print(tag.con)
# Create your views here.
def searchView(request):
    query = request.GET.get("query")
    form = SearchForm()
    search_results = None
    if query:
        search_query = SearchQuery(query, config="english")
        search_vector = SearchVector('title', weight = 'A') + SearchVector('content', weight = 'B')
        trigram_similarity=TrigramSimilarity("title", query) + TrigramSimilarity("content", query)
        ## Using Search rank
        # search_results = Post.published.annotate(search = search_vector,
        #                                          rank = SearchRank(search_vector, search_query)

        # ).filter(search=search_query).order_by('-rank')

        ## USING TrigramSimilarity
        search_results = Post.published.annotate(
            similarity=trigram_similarity
        ).filter(similarity__gt=0.2)

    context = {
        "form": form,
        "query": query,
        "results": search_results,
    }
    print("query: ", query)
    return render(request, "search.html", context)


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {}
        queryset = self.get_queryset()

        # Tags
        # Tag section
        tag = None
        try:
            tag_slug = self.kwargs["tag_slug"]
        except:
            tag_slug = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts_with_tag = Post.published.filter(tags__in=[tag])
            queryset = posts_with_tag
        context["tag"] = tag

        # Pagination

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            if int(page) < 1:
                posts = paginator.page(1)
            else:
                # If page is out of range (e.g. 9999), deliver last page of results.
                posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["page_obj"] = posts

        return context


post_list = PostListView.as_view()


class PostDetailView(DetailView):
    print("wilson is a Pastor")
    model = Post
    template_name = "post-detail.html"
    context_object_name = "post"
    queryset = Post.published.all()

    def get_object(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug = self.kwargs.get("post")
        post = get_object_or_404(
            self.get_queryset(),
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=slug,
        )
        return post

    def get_context_data(self, **kwargs: Any):

        context = super().get_context_data(**kwargs)

        context["comments"] = self.get_object().comment_set.filter(active=True)
        # Comment.objects.filter(post = self.get_object(), active = False)

        post = self.get_object()
        post_tags_ids = post.tags.values_list("id", flat=True)
        print("-----  ", post_tags_ids)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )

        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:4]
        for i in similar_posts:
            print(i, i.same_tags, i.tags.all())

        # for i in similar_posts:
        #     print(i)
        #     for k in i.tags.all():
        #         print(f"{k}")
        #         # print(k.posts)
        context["form"] = CommentForm()
        context["similar_posts"] = similar_posts
        return context


post_detail = PostDetailView.as_view()


@require_POST
def CommentView(request, post_id):
    comment = None
    form = CommentForm(request.POST)
    post = get_object_or_404(Post.published, id=post_id)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        template_name="comment.html",
        context={"comment": comment, "form": form, "post": post},
    )
    # return redirect(request.META.get("HTTP_REFERER", "/"))


def post_share(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    post_url = request.build_absolute_uri(post.get_absolute_url())

    sent = False

    print("post_uri", post_url)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            subject = f"{form_data['sender_name']} recommends you read {post.title}"
            body = f"read {post.title} at {post_url} \n \n {form_data['sender_name']}'s comment: {form_data['comment']} "
            send_mail(
                subject=subject,
                message=body,
                from_email="my_mail@mail.com",
                recipient_list=[form_data["reciever_email"]],
            )

            sent = True

    else:
        form = EmailPostForm()

    context = {"post": post, "form": form, "sent": sent}
    return render(request, template_name="post_share.html", context=context)


"""
def post_deftail(request, year, month, day, post):
    post = get_object_or_404(Post.published,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,
                             slug = post)

    return render(request=request, template_name="post-detail.html", context={"post":post})
"""
