from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {}
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

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

        context['posts'] = posts
        context['page_obj'] = posts
        
        return context

post_list = PostListView.as_view()



class PostDetailView(DetailView):
    model = Post
    template_name = 'post-detail.html'
    context_object_name = 'post'
    queryset = Post.published.all()

    def get_object(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('post')
        post = get_object_or_404(
            self.get_queryset(),
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=slug
        )
        return post
    
    def get_context_data(self, **kwargs: Any):

        context = super().get_context_data(**kwargs)
      
        context['comments'] = self.get_object().comment_set.filter(active=True)
        #Comment.objects.filter(post = self.get_object(), active = False)
        context['form'] = CommentForm()
        print(context)
        return context

post_detail = PostDetailView.as_view()

@require_POST
def CommentView(request, post_id):
    comment = None
    form = CommentForm(request.POST)
    post = get_object_or_404(Post.published, id = post_id)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, template_name="comment.html", context={'comment':comment,
                                                                  'form':form,
                                                                   'post':post})
    # return redirect(request.META.get("HTTP_REFERER", "/"))


    

def post_share(request, post_id):
    post = get_object_or_404(Post.published, id = post_id)
    post_url = request.build_absolute_uri(post.get_absolute_url())

    sent = False
   
    print("post_uri",post_url)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            subject = f"{form_data['sender_name']} recommends you read {post.title}"
            body = f"read {post.title} at {post_url} \n \n {form_data['sender_name']}\'s comment: {form_data['comment']} "
            send_mail(subject=subject, message = body,from_email = "my_mail@mail.com",recipient_list = [form_data['reciever_email']])

            sent = True

    else:
        form = EmailPostForm()

    context = {
        "post":post,
        "form":form,
        "sent":sent
    }
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