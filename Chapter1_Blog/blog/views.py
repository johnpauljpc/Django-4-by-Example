from django.shortcuts import render, get_object_or_404


from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.published.all()
    context = {"posts": posts}

    return render(request, template_name = "post_list.html", context=context)

def post_detail(request, id):
    post = get_object_or_404(Post.published, id=id)

    return render(request=request, template_name="post-detail.html", context={"post":post})
