from django.contrib import admin
from blog.models import Post, BlogComment,Tag_Blog

# Register your models here.

admin.site.register((Post, BlogComment,Tag_Blog))

