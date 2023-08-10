from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header="Epsilon Admin"
admin.site.site_title="Epsilon Admin Panel"
admin.site.index_title="Welcome to Epsilon Admin Panel"

app_name='TechBlog'

urlpatterns = [
    path('', views.TechBlogHome, name='TechBlogHome'),
    path('postTechComment', views.postTechComment, name="postTechComment"),
    path('/<str:slug>', views.TechBlogPost, name='TechBlogPost'),
    path('tag/<int:tag_id>/', views.postsByTag, name='postsByTag'),
    path('like/<int:pk>/', views.handleLike, name='handleLike'),

]
