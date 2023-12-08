from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Post
import datetime, time
from datetime import datetime
from django.db.models import F


def blog_view(request):
    now1 = datetime.now()
    posts = Post.objects.filter(published_date__lt=now1, status=1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def single_view(request, pid):
    now = datetime.now()
    posts = get_object_or_404(Post, published_date__lt=now, status=1, id=pid)
    posts.counted_view += 1
    posts.save()

    next_post = Post.objects.filter(published_date__lt=now, status=1, id__gt=pid).order_by('id').first()
    prev_post = Post.objects.filter(published_date__lt=now, status=1, id__lt=pid).order_by('-id').first()

    context = {'posts': posts, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'blog/blog-single.html', context)
        


    
