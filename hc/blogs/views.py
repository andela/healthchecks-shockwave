from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import BlogPost
from .forms import BlogPostForm
from django.utils import timezone

def post_list(request):
	blogposts = BlogPost.objects.filter(published_date__lte=timezone.now())
	page = request.GET.get('page', 1)
	paginator = Paginator(blogposts, 10)
	blogposts = paginator.page(page)
	return render(request,'blog/post_list.html', {'blogposts': blogposts})

def post_detail(request, pk):
	blogpost = get_object_or_404(BlogPost, pk=pk)
	tags = [tag.name for tag in blogpost.get_tag_names(pk)]
	return render(request, 'blog/post_detail.html', {'blogpost': blogpost, 'tags':tags} )

def post_new(request):
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		if form.is_valid():
			blogpost = form.save(commit=False)
			blogpost.author = request.user
			blogpost.published_date = timezone.now()
			blogpost.save()
			form.save_m2m()
			return redirect('hc-blog-detail', pk=blogpost.pk)
	else:
		form = BlogPostForm
	return render(request,'blog/post_new.html', {'form':form})

def post_edit(request, pk):
	blogpost = get_object_or_404(BlogPost, pk=pk)
	if request.method == "POST" and blogpost.author == request.user:		
		form = BlogPostForm(request.POST, instance=blogpost)
		if form.is_valid():
			blogpost = form.save(commit=False)
			blogpost.author = request.user
			blogpost.published_date = timezone.now()
			blogpost.save()
			form.save_m2m()
			return redirect('hc-blog-detail', pk=blogpost.pk)
	else:
		form = BlogPostForm(instance=blogpost)
	return render(request, 'blog/post_edit.html', {'form':form})

def delete_post(request, pk):
	delete_post = get_object_or_404(BlogPost, pk=pk)
	if request.user == delete_post.author:
		delete_post.delete()
		return redirect ('hc-blogs')
	else:
		return redirect('hc-blog-detail', pk=delete_post.pk)

	return redirect('hc-blog-detail', pk=delete_post.pk)
