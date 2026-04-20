from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from .models import *
from django.db.models import Q

def home(request):
    query = request.GET.get('q')

    main_news = News.objects.filter(is_main=True).order_by('-created_at')[:3]
    side_news = News.objects.filter(is_side=True).order_by('-created_at')[:4]
    breaking_news = News.objects.filter(is_breaking=True).order_by('-created_at')[:10]
    featured_news = News.objects.filter(is_featured=True).order_by('-created_at')[:8]
    trending_news = News.objects.filter(is_trending=True).order_by('-created_at')[:6]
    latest_news = News.objects.all().order_by('-created_at')

    if query:
        latest_news = latest_news.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    latest_news = latest_news[:8]
    context = {
        "main_news": main_news,
        "side_news": side_news,
        'breaking_news': breaking_news,
        'featured_news': featured_news,
        "trending_news": trending_news,
        "latest_news": latest_news,
    }
    return render(request, 'news/index.html', context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("signin")
    else:
        form = SignUpForm()
    context = {
        "form": form
    }
    return render(request, "news/signup.html", context)


def signin(request):
    form = SignInForm(data=request.POST or None)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
    context = {
        "form": form
    }
    return render(request, "news/signin.html", context)


def signout(request):
    logout(request)
    return redirect("signin")


def detail(request, slug):
    news = get_object_or_404(News, slug=slug)

    News.objects.filter(id=news.id).update(
        views_count=F('views_count') + 1
    )

    news.refresh_from_db()
    trending_news = News.objects.filter(
        is_trending=True
    ).exclude(id=news.id).order_by('-created_at')[:5]

    comments = news.comments.filter(parent__isnull=True).order_by('-created_at')

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')

        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent = None

        if name and email and text:
            Comment.objects.create(
                news=news,
                name=name,
                email=email,
                text=text,
                parent=parent
            )
        return redirect('detail', slug=slug)

    context = {
        "news": news,
        "trending_news": trending_news,
        "comments": comments,
    }

    return render(request, 'news/components/single.html', context)


def category(request, slug=None):
    selected_category = request.GET.get('category')

    trending_news = News.objects.filter(is_trending=True).order_by('-created_at')[:6]
    news = News.objects.all().order_by('-created_at')

    if selected_category:
        news = news.filter(category__slug=selected_category)

    if slug:
        news = news.filter(category__slug=slug)

    categories = Category.objects.all()
    context = {
        "news": news,
        "categories": categories,
        "trending_news": trending_news,
        "selected_category": selected_category,
    }

    return render(request, 'news/components/category.html', context)


def contact(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(full_name=full_name, email=email, subject=subject, message=message)


    return render(request, 'news/components/contact.html')
