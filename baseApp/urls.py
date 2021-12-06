from os import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('comment/<pk>/', views.comment, name='comment'),
    path('search/', views.search, name='search'),
    path('update/<pk>/', views.update, name='update'),
    path('deletePost/<pk>/', views.deletePost, name='deletePost'),
    path('deleteComment/<pk>/', views.deleteComment, name='deleteComment'),
    path('contact/', views.contact, name='contact'),
    path('pictures/<pk>/', views.pictures, name='pictures'),
    path('like/<pk>/', views.addLike, name='like'),
    path('dislike/<pk>/', views.addDislike, name='dislike'),
]