from turtle import pos
from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
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
        total_likes = post.total_likes
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            liked = True
        
    context = {
        'post' : post,
        'c_form' : c_form,
        'total_likes' : total_likes,
        'liked' : liked
    }
    return render(request, 'demo/post_details.html', context)

@login_required
def like_view(request, pk):
    post = get_object_or_404(PostModel, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return HttpResponseRedirect(reverse('blog-post-details', args=[str(pk)]))

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
    
