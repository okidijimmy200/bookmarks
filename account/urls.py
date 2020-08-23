from django.urls import path
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
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password_form.html'), name='password_change'),
    # PasswordChangeDoneView view will display a success message after the user has successfully changed his password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='password_change_done'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]