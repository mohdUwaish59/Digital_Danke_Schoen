from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
from ckeditor.fields import RichTextField
# Create your models here.

from django.db import models

# Create your models here.
class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13, null=True)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          timestamp_str = timezone.localtime(self.timeStamp).strftime("%d-%m-%Y")  # Convert to dd-mm-yyyy format
          return "Message from " + self.name + ' - ' + self.email + " on  { " + timestamp_str + " }"

class Slot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country_code = models.CharField(null=True,max_length=5)



    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"

class Client(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField()
     phone_number = models.CharField(max_length=20)
     country_code = models.CharField(null=True,max_length=5)
     unique_session_id = models.TextField()

     def __str__(self):
        return f"Session with {self.name}---{self.unique_session_id}" 

class EmailSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email         
    


class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Resume(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


def opportunity_media_upload(instance, filename):
    # Assuming 'media' is a folder within your media directory
    return os.path.join('media', filename)

class Opportunity(models.Model):
    CATEGORY_CHOICES = (
        ('study', 'Study - MS/PHD'),
        ('job', 'Job Opportunity'),
        ('scholarship', 'Scholarship - MS/PHD'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=300)
    description = RichTextField(null = True)
    media = models.FileField(upload_to=opportunity_media_upload, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        timestamp_str = timezone.localtime(self.timestamp).strftime("%d-%m-%Y")  # Convert to dd-mm-yyyy format
        return self.title + " on " + timestamp_str
