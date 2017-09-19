from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField

class Faq(models.Model):
	"""Database model to Store Frequently Asked Questions and answers"""
	question = models.CharField(max_length=200)
	answer = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.question

class Video(models.Model):
	"""Database model to store Video titles and Urls"""
	title = models.CharField(max_length=200)
	video_url = EmbedVideoField()
	created_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.title