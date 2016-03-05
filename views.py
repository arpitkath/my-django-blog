from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def post_list(request):
	posts = Post.objects.filter(date_published__lte=timezone.now()).order_by('date_published')
	return render(request, 'blog/post_list.html', {'posts' : posts})
	
@login_required
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post' : post})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(date_published__isnull=True).order_by('date_created')
	return render(request, 'blog/post_draft_list.html', {'posts' : posts})
	
@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog.views.post_detail', pk=pk)
	
@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog.views.post_list')

@login_required
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid:
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', pk=pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form' : form})