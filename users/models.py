from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    win = models.IntegerField(default=0, blank=False, null=False, verbose_name="Выигрыши")
    lose = models.IntegerField(default=0, blank=False, null=False, verbose_name="Проигрыши")
    is_private = models.BooleanField(default=False, blank=False, null=False, verbose_name="Приватность профиля")

    class Meta:
        app_label = 'users'