from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from django.utils import timezone

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now())
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 10)
	posts = paginator.page(page)
	return render(request,'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	tags = [tag.name for tag in post.get_tag_names(pk)]
	return render(request, 'blog/post_detail.html', {'post': post, 'tags':tags} )

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			form.save_m2m()
			return redirect('hc-blog-detail', pk=post.pk)
	else:
		form = PostForm
	return render(request,'blog/post_new.html', {'form':form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST" and post.author == request.user:		
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			form.save_m2m()
			return redirect('hc-blog-detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form':form})

def delete_post(request, pk):
	delete_post = get_object_or_404(Post, pk=pk)
	if request.user == delete_post.author:
		delete_post.delete()
		print('Post Deleted')
		return redirect ('hc-blogs')
	else:
		return redirect('hc-blog-detail', pk=delete_post.pk)

	return redirect('hc-blog-detail', pk=delete_post.pk)
