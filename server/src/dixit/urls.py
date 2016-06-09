
from django.conf.urls import url, include
from django.contrib import admin

from dixit import settings
import dixit.api.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(dixit.api.urls)),
]
