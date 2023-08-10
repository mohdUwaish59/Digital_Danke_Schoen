from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from blog.models import Post, BlogComment,Tag_Blog,Favorite
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from django.core.paginator import Paginator


''' 
from django.core.exceptions import ObjectDoesNotExist

try:
    post = Post.objects.get(sno=postSno)
except ObjectDoesNotExist:
    messages.error(request, "The requested blog post does not exist.")
    return redirect("some_error_url")
'''


# Create your views here.
def bloghome(request): 
    allPosts= Post.objects.order_by('-timeStamp')
    items_per_page = 12
    paginator = Paginator(allPosts, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'allPosts': allPosts, 'page_obj': page_obj}
    return render(request, "blog/blogHome.html", context)

def blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    tags = post.tags.all()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    total_comments = comments.count()
    total_replies = replies.count()

    comments_all= total_comments+total_replies
    has_liked = post.likes.filter(id=request.user.id).exists()
     # Check if likes_Number is None and set it to 0 if so
    likes_count = post.likes_Number or 0
    likes_count += post.likes.count()

    context = {
        'post': post,
        'comments': comments,
        'user': request.user,
        'replyDict': replyDict,
        'comments_all': comments_all,
        'has_liked': has_liked,
        'tags': tags,
        'post_title':post.title,
        'likes_count': likes_count
    }

    return render(request, "blog/bp.html", context)

def postsByTag(request, tag_id):
    tag = Tag_Blog.objects.get(id=tag_id)
    posts = Post.objects.filter(tags=tag)
    context = {'tag': tag, 'allPosts': posts}
    return render(request, 'blog/postsByTag.html', context)

@login_required
def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('post_Sno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parent_Sno')
        if not comment:
            messages.error(request, "Your comment can not be empty")
            return redirect(f"/blog/{post.slug}")
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")

@login_required
def handleLike(request,pk):
    blogPost = get_object_or_404(Post, sno=request.POST.get('sno'))
    blogPost.likes.add(request.user)
    return redirect(f"/blog/{blogPost.slug}", pk=pk)



def toggle_favorite(request, blog_post_id):
    if request.user.is_authenticated:
        blog_post = get_object_or_404(Post, pk=blog_post_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, blog_post=blog_post)
        if created:
            is_favorite = True
        else:
            favorite.delete()
            is_favorite = False
        return JsonResponse({'is_favorite': is_favorite})
    return JsonResponse({'error': 'Authentication required'}, status=401)

def favorites(request):
    if request.user.is_authenticated:
        favorite_posts = Post.objects.filter(favorite__user=request.user)
    else:
        favorite_posts = []
    return render(request, 'favorites.html', {'favorite_posts': favorite_posts})

