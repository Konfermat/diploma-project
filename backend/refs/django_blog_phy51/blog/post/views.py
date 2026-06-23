from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm, PostCreateForm
from  django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})

def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_details', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post/post_details.html',
                                {'post': post,
                                        'comments': comments,
                                        'form': form})
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostCreateForm()
    return render(request, 'post/post_create.html',
                                 {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', post_id=post.id)
    else:
        form = PostCreateForm(instance=post)
    return render(request, 'post/post_edit.html',
                  {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_moderator = hasattr(request.user, 'profile') and request.user.profile.is_moderator
    if request.method == 'POST':
        if request.user == post.author or is_moderator:
            if 'confirm_delete' in request.POST:
                post.delete()
                return redirect('post_list')
            else:
                return redirect('post_details', post_id=post.id)
        else:
            raise PermissionDenied

    comments = post.comments.all().order_by('-created_at')
    form = CommentForm()
    return render(request, 'post/post_details.html',
                                    {'post': post,
                                     'comments': comments,
                                     'form': form,
                                     'delete_confirm':True})