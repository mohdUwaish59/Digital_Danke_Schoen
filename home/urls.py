"""iCoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static

app_name='home'

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('RenderSignUp', views.RenderSignUp, name="RenderSignUp"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('RenderLogIn', views.RenderLogIn, name="RenderLogIn"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('available_slots', views.available_slots, name='available_slots'),
    path('slots/book/<int:slot_id>/',views.book_slot, name='book_slot'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('PDF', views.PDF, name='PDF'),
    path('after_email_subs', views.after_email_subs, name='after_email_subs'),
    path('download_pdf/<int:pdf_id>/', views.download_pdf, name='download_pdf'),
    path('Mohd_Uwaish_resume/<int:pdf_id>/', views.display_pdf_resume, name='display_pdf_resume'),
    path('opportunities', views.opportunities_home_view, name='opportunities_home'),
    path('opportunities/study - MS/PHD', views.study_opportunity_view, name='study_opportunity_view'),
    path('opportunities/job', views.job_opportunity_view, name='job_opportunity_view'),
    path('opportunities/scholarship - MS/PHD', views.scholarship_opportunity_view, name='scholarship_opportunity_view'),
    path('download_pdf_opportunity_media/<int:opportunity_id>', views.download_pdf_opportunity_media, name='download_pdf_opportunity_media'),
    path('render_forget_password', views.render_forget_password, name='render_forget_password'),
    path('reset_password_email', views.reset_password_email, name='reset_password_email'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

