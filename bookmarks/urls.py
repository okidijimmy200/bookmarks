
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    # django.contrib.auth.urls(similar to 'account/' ie /logout, /login)
    path('', include('django.contrib.auth.urls')),
]
