from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post
from TechBlog.models import TechPost
from home.models import Contact,Slot,Client,EmailSubscriber,PDFFile,Resume,Opportunity
from django.contrib.auth  import authenticate,  login, logout
from django.forms import Form, CharField, EmailField
from .forms import BookingForm, EmailSubscriptionForm
import uuid
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Use force_str instead of force_text
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Periodic deletion code
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
#ended

# Create your views here.
def home(request):
    blogPost = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
    techBlogPost = TechPost.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
    context = {'blogPostsByLike': blogPost, 'techBlogPostsByLike': techBlogPost}
    return render(request, 'home/home.html', context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if name is None:
            messages.error(request, "Please Enter your name")
        elif email is None:
            messages.error(request, "Please enter your Email")
        elif len(phone)<10 or phone is None:
            messages.error(request, "Please Enter you contact detail correctly with country code")
        elif phone[0] !='+':
            messages.error(request, "Please Enter country code with + in beginning")    
        elif content is None:
            messages.error(request, "Please Enter content of your query/message")    
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your Message/Query has been successfully sent, We will revert back to you soon")
            return redirect("/")
    return render(request, "home/contact.html")

def about(request): 
    resume = Resume.objects.get(pk=1)
    return render(request, 'home/about.html',{'resume': resume})

def search(request):
    query=request.GET['query']
    if len(query)>80 or len(query)==0:
        allPosts=Post.objects.none()
        allTechPosts=TechPost.objects.none()
    else:
        #For Blog App
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
        #For Tech Blog App
        allTechPostsTitle= TechPost.objects.filter(title__icontains=query)
        allTechPostsAuthor= TechPost.objects.filter(author__icontains=query)
        allTechPostsContent =TechPost.objects.filter(content__icontains=query)
        allTechPosts=  allTechPostsTitle.union(allTechPostsContent, allTechPostsAuthor)

    if allPosts.count() ==0 and allTechPosts.count()==0:
        if len(query)>80:
            messages.warning(request, "No search results found. Please refine your query.")
        elif len(query)==0:
            messages.warning(request, "Search text is empty, Please enter a query in search text field")    
    params={'allPosts': allPosts, 'allTechPosts':allTechPosts, 'query': query}
    return render(request, 'home/search.html', params)

def RenderSignUp(request):
    return render(request, 'home/signup.html')
    
#change
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if User.objects.filter(username__icontains=username):
            messages.error(request, "Please choose a unique username as This username is already taken")
            return redirect('/')
        if len(username)>30:
            messages.error(request, " Your user name must be under 30 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('/')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, f" Your account has been successfully created with username {username}")
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")    



def RenderLogIn(request):
    request.session['previous_page_url'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'home/login.html')


def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            previous_page_url = request.session.get('previous_page_url', '/')
            return redirect(previous_page_url)
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")
    #return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def render_forget_password(request):
    return render(request, 'home/forget_password.html')


User = get_user_model()

def reset_password_email(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            # Use get_object_or_404 or proper validation to check if the email exists in the User model
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Avoid exposing email existence through error messages
            messages.error(request, f"The provided email does not exist in our records, Kindly enter correct Email ID")
        else:
            # Generate a password reset token for the user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_password_link = f"http://{get_current_site(request).domain}/reset_password/{uid}/{token}/"

            subject = 'Password Reset Link'
            html_message = render_to_string('home/reset_password_email.html', {
                'receiver': email,
                'reset_password_link': reset_password_link,
            })

            # Create the EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, html_message, 'goodhomelander@gmail.com', [email])
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()

            messages.success(request, f"An email with the link to reset your password has been sent to your Email ID.")
            return redirect("/")

    return render(request, 'home/forget_password.html')
                


User = get_user_model()

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # If the user and token are valid, handle the password reset process here
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                messages.success(request, "Your password has been reset successfully.")
                return redirect('/')
            else:
                messages.error(request, "Passwords do not match. Please try again.")
    else:
        messages.error(request, "Invalid password reset link. Please try again.")
    
    return render(request, 'home/reset_password.html')


def available_slots(request):
    slots = Slot.objects.filter(is_available=True)
    return render(request, 'home/available_slots.html', {'slots': slots})

def generate_session_id():
    session_id = str(uuid.uuid4())
    return session_id

def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, pk=slot_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            slot.is_available = False
            slot.name = form.cleaned_data['name']
            slot.email = form.cleaned_data['email']
            slot.phone_number = form.cleaned_data['phone_number']
            slot.country_code = form.cleaned_data['country_code']

            session_id = generate_session_id()
            myclient=Client(name=slot.name,email=slot.email,phone_number=slot.phone_number,
                            country_code=slot.country_code,unique_session_id=session_id)
            slot.session_id = session_id
            slot.save()
            myclient.save()

            # Send the confirmation email with reference ID
            subject = '1:1 personal consultation session confrimation'
            html_message = render_to_string('home/book_slot_email.html', {
                'reciever': slot.email,
                'session_id': session_id,
            })

            # Create the EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, html_message, "noreply@digitaldankeschoen.com", [slot.email])
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()
            messages.success(request, f"A session has been booked with unique reference ID: {session_id}")
            return redirect('/')
    else:
        form = BookingForm()

    return render(request, 'home/book_slot.html', {'slot': slot, 'form': form})



def booking_success(request):
    return render(request, 'home/booking_success.html')



def PDF(request):
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber = EmailSubscriber.objects.create(email=email)
            pdf_file = get_object_or_404(PDFFile, id=1)
            # Generate the download link
            download_link = f"http://{get_current_site(request).domain}/download_pdf/{pdf_file.id}/"

            # Send the verification email with download link
            subject = 'Free PDF E-book for Study in Germany by DigitalDanke Schön'
            html_message = render_to_string('home/verification_email.html', {
                'subscriber': subscriber,
                'download_link': download_link,
            })

            # Create the EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, html_message, 'goodhomelander@gmail.com', [email])
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()

            messages.success(request, "An email has been sent to your provided email ID (check spam folder also), Kindly click on Download button to download the PDF. ")
            return redirect(f"/after_email_subs")
    else:
        form = EmailSubscriptionForm()

    return render(request, 'home/subscribe.html', {'form': form})


def download_pdf(request, pdf_id):
    try:
        pdf_file = PDFFile.objects.get(pk=pdf_id)
    except PDFFile.DoesNotExist:
        return HttpResponse("PDF file not found.", status=404)

    response = HttpResponse(pdf_file.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_file.file}"'
    return response


def download_pdf_opportunity_media(request, opportunity_id):
    try:
        opportunity = Opportunity.objects.get(pk=opportunity_id)
        if opportunity.media and opportunity.media.url.lower().endswith('.pdf'):
            # Retrieve the media file URL and filename
            media_url = opportunity.media.url
            filename = opportunity.media.name.split('/')[-1]  # Get the filename from the media URL

            # Create the HTTP response for downloading the PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Open the media file and write its content to the response
            with opportunity.media.open(mode='rb') as media_file:
                response.write(media_file.read())

            return response
        else:
            return HttpResponse("PDF file not found.", status=404)
    except ObjectDoesNotExist:
        return HttpResponse("Opportunity not found.", status=404)


def after_email_subs(request):
    return redirect(f"/")


def display_pdf_resume(request, pdf_id):
    pdf_doc = Resume.objects.get(pk=1)
     # Check if the user has permission to access the PDF (optional, you can implement your own logic here)
    # Serve the PDF data using Django's serve function
    response = HttpResponse(pdf_doc.file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Mohd Uwaish Resume.pdf"'
    return response

def opportunities_home_view(request):
    opportunities_study = Opportunity.objects.filter(category='study').order_by('-timestamp')[:10]
    opportunities_job = Opportunity.objects.filter(category='job').order_by('-timestamp')[:10]
    opportunities_scholarship = Opportunity.objects.filter(category='scholarship').order_by('-timestamp')[:10]

    context = {
        'os':  opportunities_study,
        'oj': opportunities_job,
        'osc':opportunities_scholarship,
        'media_url': '/media/'
         }
    return render(request, 'home/opportunities_home.html', context)

def study_opportunity_view(request):
    opportunities = Opportunity.objects.filter(category='study')
    opportunities=opportunities.order_by('-timestamp')

    items_per_page = 15
    paginator = Paginator(opportunities, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'opportunities': opportunities, 
        'category': 'Study - MS/PHD',
        'page_obj':page_obj, 
        'media_url': '/media/'
        }

    return render(request, 'home/opportunities_section.html', context)

def job_opportunity_view(request):
    opportunities = Opportunity.objects.filter(category='job')
    opportunities=opportunities.order_by('-timestamp')

    items_per_page = 15
    paginator = Paginator(opportunities, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'opportunities': opportunities, 
        'category': 'Job Opportunities',
        'page_obj':page_obj, 
        'media_url': '/media/'
        }
    
    return render(request, 'home/opportunities_section.html', context)

def scholarship_opportunity_view(request):
    opportunities = Opportunity.objects.filter(category='scholarship')
    opportunities=opportunities.order_by('-timestamp')

    items_per_page = 15
    paginator = Paginator(opportunities, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'opportunities': opportunities, 
        'category': 'Scholarship Announcements',
        'page_obj':page_obj, 
        'media_url': '/media/'
        }
    return render(request, 'home/opportunities_section.html',context)

#Periodic deletion
def delete_old_opportunities():
    one_month_ago = timezone.now() - timedelta(days=45)
    expired_opportunities = Opportunity.objects.filter(timestamp__lt=one_month_ago)
    expired_opportunities.delete()