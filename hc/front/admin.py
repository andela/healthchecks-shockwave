from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Faq, Video
# Register your models here.
class FaqAdmin(admin.ModelAdmin):
	list_display = ('question', 'answer', 'created_date')

class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
	list_display = ('title', 'video_url', 'created_date')

admin.site.register(Faq, FaqAdmin)
admin.site.register(Video, VideoAdmin)
