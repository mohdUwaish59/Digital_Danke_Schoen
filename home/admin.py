from django.contrib import admin
from .models import Contact,Slot ,EmailSubscriber,Client, PDFFile,Resume,Opportunity

# Register your models here.

admin.site.register(Contact)
admin.site.register(Slot)
admin.site.register(Client)
admin.site.register(EmailSubscriber)
admin.site.register(PDFFile)
admin.site.register(Resume)
admin.site.register(Opportunity)