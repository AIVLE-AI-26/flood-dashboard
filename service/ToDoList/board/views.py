from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, HttpResponse
from urllib.parse import quote
from .models import Post
from .forms import PostForm
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required

import os
import time
from django.conf import settings
def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    return render(request, 'main/notice.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()

    file_url = post.file.url if post.file else None
    file_type = guess_type(file_url)[0] if file_url else None
    is_image = file_type and file_type.startswith('image')

    if is_image or file_url:
        file_name = os.path.basename(file_url)
    else:
        file_name = None

    return render(request, 'board/post_detail.html', {
        'post': post,
        'is_image': is_image,
        'file_url': file_url,
        'file_name': file_name  
    })
    

def download_file(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.file:
        raise Http404("File not found")

    file_path = post.file.path

    file_type, _ = guess_type(file_path)
    if not file_type:
        file_type = 'application/octet-stream' 

    try:
        response = FileResponse(open(file_path, 'rb'), content_type=file_type)
        encoded_file_name = quote(os.path.basename(file_path))
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_file_name}'
        return response
    except FileNotFoundError:
        raise Http404("File not found")


    

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/write.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form, 'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

