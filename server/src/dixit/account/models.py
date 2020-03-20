
from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    name = models.CharField(max_length=64, verbose_name=_('name'))
