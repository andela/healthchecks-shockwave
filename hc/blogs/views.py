from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import BlogPost, Tag
from .forms import BlogPostForm
from django.utils import timezone

def post_list(request, tag_slug=None):
	"""
	Returns list of blogs that exist in the database.
	Takes optional tag_slug to filter posts with a particular tag.
	@tag_slug: : to be used when filtering posts
	"""
	blogposts = BlogPost.objects.filter(published_date__lte=timezone.now())
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		blogposts = blogposts.filter(tags__in=[tag])
	page = request.GET.get('page', 1)
	paginator = Paginator(blogposts, 12)
	blogposts = paginator.page(page)
	return render(request,'blog/post_list.html', locals())

def post_detail(request, pk):
	""" Displays single blog post"""
	blogpost = get_object_or_404(BlogPost, pk=pk)
	tags = [tag.name for tag in blogpost.get_tag_names(pk)]
	return render(request, 'blog/post_detail.html', {'blogpost': blogpost, 'tags':tags} )

def post_new(request):
	"""Creates new blog post"""
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		form_valid(form, request.user)
	else:
		form = BlogPostForm
	return render(request,'blog/post_new.html', {'form':form})

def post_edit(request, pk):
	"""Updates or Edits Blogpost"""
	blogpost = get_object_or_404(BlogPost, pk=pk)
	if request.method == "POST" and blogpost.author == request.user:
		form = BlogPostForm(request.POST, instance=blogpost)
		form_valid(form, request.user)
	else:
		form = BlogPostForm(instance=blogpost)
	return render(request, 'blog/post_edit.html', {'form':form})

def delete_post(request, pk):
	"""Deletes healthchecks blog post"""
	delete_post = get_object_or_404(BlogPost, pk=pk)
	if request.user == delete_post.author:
		delete_post.delete()
		return redirect ('hc-blogs')
	else:
		return redirect('hc-blog-detail', pk=delete_post.pk)
	return redirect('hc-blog-detail', pk=delete_post.pk)

def form_valid(form, user):
	if form.is_valid():
		blogpost = form.save(commit=False)
		blogpost.author = user
		blogpost.published_date = timezone.now()
		blogpost.save()
		form.save_m2m()
		return redirect('hc-blog-detail', pk=blogpost.pk)
