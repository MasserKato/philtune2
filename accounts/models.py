from django.contrib.auth.models import AbstractUser
from django.db import models


class Instrument(models.Model):
    name = models.CharField(verbose_name='楽器', max_length=20)
    section_name = models.CharField(verbose_name='セクション', max_length=10)
    short_name = models.CharField(verbose_name='楽器の略称', max_length=10, default='?')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    nick_name = models.CharField(verbose_name='表示名', max_length=10, blank=True, null=True)
    bio = models.TextField(verbose_name='ひとこと', max_length=100, blank=True, null=True)
    instrument = models.ForeignKey(Instrument, verbose_name='パート', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'CustomUser'

    def __str__(self):
        return self.name
