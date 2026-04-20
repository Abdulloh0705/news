from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("email must be fill")
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Staff status must be True")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Super User status must be True")
        return self.create_user(email=email, password=password, **kwargs)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(upload_to='news/')
    content = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    is_side = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class NewsDetail(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='details')

    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='news/details/', blank=True, null=True)

    def __str__(self):
        return f"{self.news.title} - detail"
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()

    def __str__(self):
        return self.full_name