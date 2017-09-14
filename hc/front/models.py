from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField

# Create your models here.
class Faq(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.question

class Video(models.Model):
	title = models.CharField(max_length=200)
	video_url = EmbedVideoField()
	created_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.title