from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('news/<slug:slug>/', detail, name='detail'),
    path('category/', category, name='category'),
    path('category/<slug:slug>/', category, name='category_slug'),
    path('contact/', contact, name='contact'),
]
