from django.shortcuts import redirect, render
from django import forms
from django.http.response import HttpResponse
from .models import PostModel
from .forms import CommentForm, PostModelForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def hello(request):
    post = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('/blog')
    else:
        form = PostModelForm
    context = {
        'posts' : post,
        'form' : form

    }
    return render(request, 'demo/index.html', context)

@login_required
def post_details(request,pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form. is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog-post-details', pk = post.id)
    else:
        c_form = CommentForm()
    context = {
        'post' : post,
        'c_form' : c_form
    }
    return render(request, 'demo/post_details.html', context)

@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post-details', pk = post.id)

    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post' : post,
        'form' : form
    }
    return render(request, 'demo/post_edit.html', context)

@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog')
    context = {
        'post' : post
    }
    return render(request, 'demo/post_delete.html', context)

def social_share(request,pk):
    post = PostModel.objects.get(id=pk)
    context = {
        'post' : post
    }
    return render(request,'social.html', context)

def myblogs(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    posts = PostModel.objects.filter(author=user)
    context = {
        'posts' : posts
    }
    return render(request, 'demo/myblogs.html', context)
    