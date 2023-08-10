from django.contrib import admin
from TechBlog.models import TechPost,Tag,TechBlogComment
# Register your models here.

admin.site.register((TechPost,Tag,TechBlogComment))