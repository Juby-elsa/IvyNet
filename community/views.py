from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages

def community_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'community/feed.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(author=request.user.profile, content=content, image=image)
        messages.success(request, "Post shared with the community!")
        return redirect('community_feed')
    return render(request, 'community/create_post.html')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)
    return redirect('community_feed')

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user.profile, text=text)
    return redirect('community_feed')
