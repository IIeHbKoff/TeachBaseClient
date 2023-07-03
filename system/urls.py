from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/client/v1/', include('apps.client.v1.urls'))
]
