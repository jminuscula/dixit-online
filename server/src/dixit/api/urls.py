
from django.conf.urls import url, include


urlpatterns = [
    url(r'^game/', include('dixit.api.game.urls')),
    url(r'^user/', include('dixit.api.auth.urls')),
]
