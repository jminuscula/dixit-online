
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('dixit.accounts.urls')),
    url(r'^api/', include('dixit.api.urls')),
]
