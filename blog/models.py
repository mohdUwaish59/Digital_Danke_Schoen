from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone

class Tag_Blog(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=14)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=RichTextField(blank= True, null= True)
    likes_Number=models.IntegerField(null=True)
    tags = models.ManyToManyField('Tag_Blog', related_name='tab_blog')
    likes = models.ManyToManyField(User,related_name='blog_posts')
    #content=models.TextField()
  

    def __str__(self):
        return self.title + " by " + self.author

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        truncated_comment = self.comment[:13] + "..." if len(self.comment) > 13 else self.comment
        timestamp_str = timezone.localtime(self.timestamp).strftime("%d-%m-%Y")  # Convert to dd-mm-yyyy format
        return f"{truncated_comment} by {self.user.username} on {timestamp_str}"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.blog_post.title}"
