
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    # django.contrib.auth.urls(similar to 'account/' ie /logout, /login)
    path('', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

# NB:The static() helper function is suitable for development, but not for
# production use. Never serve your static files with Django in a production
# environment.