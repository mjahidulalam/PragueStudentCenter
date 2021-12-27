
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('user.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})


] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)