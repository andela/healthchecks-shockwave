# from django.test import TestCase
from django.shortcuts import render, get_object_or_404, redirect
from hc.test import BaseTestCase
from django.views.generic import ListView
from hc.blogs.models import Post
from hc.blogs.forms import PostForm
# from hc.blogs.views import post

class BlogTestCase(BaseTestCase):
	URL = "/blog/"
	def setUp(self):
		super(BlogTestCase, self).setUp()
		Post.objects.create(title="Trravelling",text="Nairobi", \
				tags="Cities", author=self.alice)
		Post.objects.create(title="Teams",text="IT Teams", \
				tags="Tech", author=self.alice)

	def test_blog_url(self):
		response = self.client.get('/blog/')
		self.assertEquals(response.status_code, 200)

	def test_create_blog_post(self):
		Post.objects.create(title="Trravelling",text="Nairobi", \
				tags="Cities", author=self.alice)
		response = self.client.get('/blog/')
		self.assertEquals(response.status_code, 200)
		post = Post.objects.all()
		self.assertEquals(len(post), 3)
		response = self.client.get('/blog/post/3/')

	def test_update_blog_post(self):
		post = Post.objects.first()
		post_id = post.id
		post.title = "Travelling to Kenya"
		post.text = "Visit Nairobi"
		post.save()
		post = Post.objects.get(id=post_id)
		self.assertEquals(post.title, "Travelling to Kenya")
		self.assertEquals(post.text, "Visit Nairobi")


	def test_delete_blog_post(self):
		post =Post.objects.all()
		num_posts_before_print = len(post)
		post = Post.objects.first()
		post.delete()
		self.assertEquals(len(Post.objects.all()), 1)
		







