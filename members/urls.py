from django.urls import path
from . import views
from django.contrib.auth import views as authViews


urlpatterns = [
    path('loginUser/', views.loginUser, name='loginUser'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('registerUser/', views.registerUser, name='registerUser'),
    
    path('reset_password/', authViews.PasswordResetView.as_view(
        template_name='authenticate/reset_password.html'), name='reset_password'),
    
    path('password_reset/done/', authViews.PasswordResetDoneView.as_view(
        template_name='authenticate/reset_password_done.html'), name='reset_password_done'),
    
    path('reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(
        template_name='authenticate/reset_password_confirm.html'), name='reset_password_confirm'),
    
    path('reset/done/', authViews.PasswordResetCompleteView.as_view(
        template_name='authenticate/reset_password_complete.html'), name='reset_password_complete'),
]