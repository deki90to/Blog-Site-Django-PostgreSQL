from django.shortcuts import redirect, render
from . models import *
from . forms import *
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, Paginator
from django.contrib.auth.models import User


def home(request):
    if request.method == 'GET':
        # posts = Post.objects.all()
        participants = Comment.objects.all()
        
        p = Paginator(Post.objects.all(), 5)
        page = request.GET.get('page')
        
        try:
            posts = p.get_page(page)
        except EmptyPage:
            posts = p.get_page(p.num_pages)
        
    if request.method == 'POST':
        post = Post.objects.create(
            user=request.user,
            post=request.POST['post'],
            image=request.FILES.get('image')
        )
        messages.success(request, '✔Posted')
        return redirect('home')        

    context = {'posts': posts, 'participants': participants, 'posts': posts}
    return render(request, 'baseApp/home.html', context)



@login_required(login_url='loginUser')
def comment(request, pk):
    # posts = Post.objects.all()
    participants = Comment.objects.all()
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    
    p = Paginator(Post.objects.all(), 10)
    page = request.GET.get('page')
    
    try:
        posts = p.get_page(page)
    except EmptyPage:
        posts = p.get_page(p.num_pages)
    
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            comment=request.POST['comment'],
            )
        messages.success(request, '✔Commented')
        return redirect('comment', pk=post.id)
    
    context = {'post': post, 'comments': comments, 'posts': posts, 'participants': participants, 'page': page}
    return render(request, 'baseApp/home.html', context)



@login_required(login_url='loginUser')
def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searched = Post.objects.filter(Q(post__icontains=q))
    
    context = {'searched': searched, 'q': q}
    return render(request, 'baseApp/search.html', context)



@login_required(login_url='loginUser')
def update(request, pk):
    posts = Post.objects.all()
    updatePost = Post.objects.get(pk=pk)
    form = PostForm(instance=updatePost)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=updatePost)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated!')
            return redirect('home')
    
    context = {'form': form, 'updatePost': updatePost, 'posts': posts}
    return render(request, 'baseApp/updatePost.html', context)



@login_required(login_url='loginUser')
def deletePost(request, pk):
    deletePost = Post.objects.get(pk=pk)
    posts = Post.objects.all()
    participants = Comment.objects.all()
    
    if request.method == 'POST':
        deletePost.delete()
        messages.success(request, 'Post Deleted!')
        return redirect('home')

    context = {'deletePost': deletePost, 'posts': posts, 'participants': participants}
    return render(request, 'baseApp/deletePost.html', context)



@login_required(login_url='loginUser')
def deleteComment(request, pk):
    comment = Comment.objects.get(pk=pk)
    posts = Post.objects.all()
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment Deleted!')
        return redirect('comment', pk=comment.post.pk)

    context = {'comment': comment, 'posts': posts}
    return render(request, 'baseApp/deleteComment.html', context)



def contact(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            subject,
            message,
            email,
            ['deki90to@gmail.com']
        )
        messages.success(request, 'Your message/suggestion was sent!')
        return render(request, 'baseApp/home.html', {'email': email, 'message': message})
    else:
        return render(request, 'baseApp/contact.html')
    
    
    
@login_required(login_url='loginUser')
def pictures(request, pk):
    post = Post.objects.get(pk=pk)
    
    context = {'post': post}
    return render(request, 'baseApp/pictures.html', context)




@login_required(login_url='loginUser')
def addLike(request, pk):
    post = Post.objects.get(pk=pk)
    next = request.POST.get('next', '/')
    
    isDislike = False
    
    for dislike in post.dislikes.all():
        if dislike == request.user:
            isDislike = True
            break
    if isDislike:
        post.dislikes.remove(request.user)
    
    isLike = False
    
    for like in post.likes.all():
        if like == request.user:
            isLike = True
            break
    if not isLike:
        post.likes.add(request.user)
    if isLike:
        post.likes.remove(request.user)
        
    return redirect(next)



@login_required(login_url='loginUser')
def addDislike(request, pk):
    post = Post.objects.get(pk=pk)
    next = request.POST.get('next', '/')

    isLike = False
    
    for like in post.likes.all():
        if like == request.user:
            isLike = True
            break
    if isLike:
        post.likes.remove(request.user)
        
    isDislike = False
    
    for dislike in post.dislikes.all():
        if dislike == request.user:
            isDislike = True
            break
    if not isDislike:
        post.dislikes.add(request.user)
    if isDislike:
        post.dislikes.remove(request.user)
        
    return redirect(next)



@login_required(login_url='loginUser')
def myProfile(request):
    posts = Post.objects.all()
    user_profile = UserProfile.objects.all()
    return render(request, 'baseApp/myProfile.html', {'posts': posts, 'user_profile': user_profile})



@login_required(login_url='loginUser')
def myProfileForm(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        user = request.user
        image=request.FILES.get('userProfileImage')
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        user_profile = UserProfile(
            user=user,
            profile_image=image,
            first_name=firstname,
            last_name=lastname,
            email=email,
            phone=phone,
        )
        user_profile.save()
        return redirect('myProfile')

    return render(request, 'baseApp/myProfileForm.html', {'posts': posts})



def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    user_profile = user.userprofile_set.all()
    return render(request, 'baseApp/userProfile.html', {'user': user, 'user_profile': user_profile})