from django.urls import path, include
from django.contrib.auth import views as auth_views
from .import views



urlpatterns = [
    # post views (previous login view)
    # path('login/', views.user_login, name='login'), 
    # ---use the LoginView view of Django's authentication framework.
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),    
    ################# change password urls ###################
    # The PasswordChangeView view will handle the form to change the password,
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password_form.html'), name='password_change'),
    # PasswordChangeDoneView view will display a success message after the user has successfully changed his password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='password_change_done'),

     # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.dashboard, name='dashboard'),

    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]