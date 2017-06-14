from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, HttpResponseRedirect, redirect
from post.models import Post
from post.forms import PostForm, CommentFrom
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.

def post_index(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)
                                     ).distinct()

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts =paginator.page(paginator.num_pages)

    return render(request, 'post/index.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentFrom(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'post/detail.html', context)


def post_create(request):
   if not request.user.is_authenticated():
       return Http404()

   if request.method == "POST":
       form = PostForm(request.POST or None, request.FILES or None)
       if form.is_valid():
           kayit = form.save(commit=False)
           kayit.user = request.user
           kayit.save()
           messages.success(request, 'Başarı bir şekilde oluşturdun ', extra_tags='mesaj-basarili')
           return HttpResponseRedirect(kayit.get_absolute_url())
   else:
       form = PostForm()
    #form = PostForm(request.POST or none)
    # if form.is_valid():
       #form.save()
   context = {
       'form': form,
   }
   return render(request, 'post/form.html', context)


def post_update(request, slug):
    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,  request.FILES or None, instance=post)
    if form.is_valid():
        kayit = form.save()
        messages.success(request, 'Başarı bir şekilde güncelledin ', extra_tags='mesaj-basarili')
        return HttpResponseRedirect(kayit.get_absolute_url())
    context = {
        'form' : form
    }
    return render(request, 'post/form.html', context)


def post_delete(request, slug):
    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')
