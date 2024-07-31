from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def home_page(request):
    posts = Post.objects.filter(is_visible=True).order_by('-created_at')

    context = {
        "posts": posts
    }
    return render(request,"home_page.html",context)

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    
    context = {
        "post": post
    }
    return render(request,"post_detail.html",context)

@login_required
def post_new(request):
    if request.method != "POST":
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", post_id = post.pk)
    return render(request, "post_new.html", {"form":form})


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.pk != post.author.pk:
        return redirect("/403")
    
    if request.method != "POST":
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.edited = True
            post.save()
            return redirect("post_detail", post_id = post.pk)
    context = {
        'form':form,
    }
    return render(request, 'post_new.html', context)

def post_confirm_delete(request, post_id):
    context = {
        'post_id':post_id,
    }
    return render(request, "post_confirm_delete.html",context)

def post_delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.pk != post.author.pk:
        return redirect("/403")
    post.delete()
    return redirect('home_page')