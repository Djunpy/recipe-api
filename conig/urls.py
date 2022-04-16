from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls', namespace='users')),
    path('api/recipe/', include('recipe.urls', namespace='recipe')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/password/reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
