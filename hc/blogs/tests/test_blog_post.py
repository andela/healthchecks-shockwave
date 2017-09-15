# from django.test import TestCase
from django.shortcuts import render, get_object_or_404, redirect
from hc.test import BaseTestCase
from django.views.generic import ListView
from hc.blogs.models import BlogPost
from hc.blogs.forms import BlogPostForm

class BlogTestCase(BaseTestCase):
	URL = "/blog/"
	def setUp(self):
		super(BlogTestCase, self).setUp()
		BlogPost.objects.create(title="Trravelling",text="Nairobi", \
				tags="Cities", author=self.alice)
		BlogPost.objects.create(title="Teams",text="IT Teams", \
				tags="Tech", author=self.alice)
		self.URL = "/blog/"

	def test_blog_url(self):
		response = self.client.get(self.URL)
		self.assertEquals(response.status_code, 200)

	def test_create_blog_post(self):
		BlogPost.objects.create(title="Trravelling",text="Nairobi", \
				tags="Cities", author=self.alice)
		response = self.client.get(self.URL)
		self.assertEquals(response.status_code, 200)
		post_id = str(BlogPost.objects.last().pk)
		post = BlogPost.objects.all()
		self.assertEquals(len(post), 3)
		response = self.client.get(self.URL+'post/' + post_id +'/')
		self. assertEquals(response.status_code, 200)
		print(type(response.content))
		self.assertIn("Nairobi",response.content.decode('ascii'))

	def test_update_blog_post(self):
		post = BlogPost.objects.first()
		post_id = post.id
		post.title = "Travelling to Kenya"
		post.text = "Visit Nairobi"
		post.save()
		post = BlogPost.objects.get(id=post_id)
		self.assertEquals(post.title, "Travelling to Kenya")
		self.assertEquals(post.text, "Visit Nairobi")

	def test_delete_blog_post(self):
		post = BlogPost.objects.all()
		num_posts_before_print = len(post)
		post = BlogPost.objects.first()
		post.delete()
		self.assertEquals(len(BlogPost.objects.all()), 1)
		







