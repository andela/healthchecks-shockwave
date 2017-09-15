from django.conf.urls import url
from .import views

urlpatterns=[
    url(r'^$', views.post_list, name='hc-blogs'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name = 'hc-blog-detail'),
    url(r'post/new/', views.post_new,name ='hc-blog-add'),
    url(r'post/(?P<pk>\d+)/edit/', views.post_edit, name = 'hc-blog-edit'),
    url(r'post/(?P<pk>\d+)/delete/', views.delete_post, name = 'hc-blog-delete'),
]