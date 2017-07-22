
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from dixit.api.auth.views.user import Me


urlpatterns = [
    url(r'^me/', Me.as_view()),

    url(r'^api-token-auth/', obtain_jwt_token),
]
