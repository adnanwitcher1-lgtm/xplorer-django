from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Xplorer Solution Admin"
admin.site.site_title = "Xplorer Admin"
admin.site.index_title = "Website Content Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("agency.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
