from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header="Epsilon Admin"
admin.site.site_title="Epsilon Admin Panel"
admin.site.index_title="Welcome to Epsilon Admin Panel"
#app_name='Blog'

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', views.bloghome, name="bloghome"),
    path('/<str:slug>', views.blogpost, name="blogpost"),
    path('tag/<int:tag_id>/', views.postsByTag, name='postsByTag'),
    path('like/<int:pk>/', views.handleLike, name='handleLike'),
    path('<int:blog_post_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
]
