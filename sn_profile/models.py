from django.db import models
from django.contrib.auth.models import User


class SocialNetworkProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)


User.sn_profile = property(lambda u: SocialNetworkProfile.objects.get_or_create(user=u)[0])
