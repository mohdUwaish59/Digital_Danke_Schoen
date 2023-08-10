from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from TechBlog.models import TechPost,Tag,TechBlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.
def TechBlogHome(request):
    allPosts= TechPost.objects.order_by('-timeStamp')
    items_per_page = 12
    paginator = Paginator(allPosts, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'allPosts': allPosts, 'page_obj': page_obj}
    return render(request, "techblog/techBlogHome.html", context)


def TechBlogPost(request, slug): 
    post = TechPost.objects.filter(slug=slug).first()
    tags = post.tags.all()
    comments = TechBlogComment.objects.filter(post=post, parent=None)
    replies = TechBlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    total_comments = comments.count()
    total_replies = replies.count()
    comments_all = total_comments + total_replies
    has_liked = post.likes.filter(id=request.user.id).exists()
     # Check if likes_Number is None and set it to 0 if so
    likes_count = post.likes_Number or 0
    likes_count += post.likes.count()

    context = {
        'post': post, 
        'tags': tags,
        'comments': comments,
        'user': request.user, 
        'replyDict': replyDict, 
        'has_liked': has_liked,
        'comments_all': comments_all,
        'post_title': post.title,
        'likes_count': likes_count
    }

    return render(request, "techblog/TempPost.html", context)


def postsByTag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    posts = TechPost.objects.filter(tags=tag)
    context = {'tag': tag, 'allPosts': posts}
    return render(request, 'techblog/postsByTag.html', context)

def handleLike(request,pk):
    techPost = get_object_or_404(TechPost, sno=request.POST.get('sno'))
    techPost.likes.add(request.user)
    return redirect(f"/techblog/{techPost.slug}", pk=pk)


def postTechComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('post_Sno')
        post = TechPost.objects.get(sno=postSno)
        parentSno= request.POST.get('parent_Sno')
        if not comment:
            messages.error(request, "Your comment can not be empty")
            return redirect(f"/techblog/{post.slug}")
        if parentSno=="":
            comment=TechBlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= TechBlogComment.objects.get(sno=parentSno)
            comment=TechBlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")  
    return redirect(f"/techblog/{post.slug}")








