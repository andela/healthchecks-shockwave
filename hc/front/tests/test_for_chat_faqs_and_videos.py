import os 
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from hc.test import BaseTestCase
from hc.front.models import Faq, Video


class HelpCenterTestCase(BaseTestCase):
	def setUp(self):
		super(HelpCenterTestCase, self).setUp()
		self.URL = "/help/"

	def test_help_page_exists(self):
		response = self.client.get(self.URL)
		self.assertEqual(response.status_code, 200)
		self.assertIn("Welcome to Healthchecks Help Center", 
					response.content.decode('ascii'))
		self.assertIn("Frequently Asked Questions", 
					response.content.decode('ascii'))
		self.assertIn("Videos", 
					response.content.decode('ascii'))

	def test_creating_faq(self):
		Faq.objects.create(question="How do I create a Check?", 
			answer="Healthchecks is a cronjob Monitoring Service")

		response = self.client.get(self.URL+"faqs/")
		self.assertEqual(response.status_code, 200)
		self.assertIn("How do I create a Check", 
					response.content.decode('ascii'))
		self.assertIn("Healthchecks is a cronjob Monitoring Service", 
					response.content.decode('ascii'))
	def test_creating_and_displaying_video(self):
		Video.objects.create(title="Video 1: Creating a Check", 
			video_url="https://www.youtube.com/ \
			            watch?v=--Pr7-2Ul_k&feature=youtu.be")
		response = self.client.get(self.URL + "videos/")
		self.assertEqual(response.status_code, 200)
		self.assertIn("Video 1: Creating a Check", 
					response.content.decode('ascii'))
		
	def test_displaying_single_video(self):
		Video.objects.create(title="Video 1: Creating a Check", 
			video_url="https://www.youtube.com/ \
			            watch?v=--Pr7-2Ul_k&feature=youtu.be")
		video_id = str(Video.objects.first().pk)
		response = self.client.get(self.URL + "video/" + video_id + "/")
		self.assertEqual(response.status_code, 200)
		self.assertIn("Video 1: Creating a Check",
				response.content.decode('ascii'))
	def test_chat_is_displayed_on_the_web_page(self):
		response = self.client.get(self.URL)
		self.assertIn("http://my.clickdesk.com/clickdesk-ui/browser/",
			response.content.decode("ascii"))


