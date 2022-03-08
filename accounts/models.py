from django.contrib.auth.models import AbstractUser
from django.db import models


class Part(models.Model):
    class Meta:
        db_table = 'part'
        verbose_name = verbose_name_plural = 'パート'
    
    name = models.CharField(verbose_name='パート名', max_length=40)
    short_name = models.CharField(verbose_name='パート名(略称)', max_length=10)
    wind = models.BooleanField(verbose_name='管楽器である')
    brass = models.BooleanField(verbose_name='金管楽器である')
    woodwind = models.BooleanField(verbose_name='木管楽器である')
    string = models.BooleanField(verbose_name='弦楽器である')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    nick_name = models.CharField(verbose_name='表示名', max_length=10, blank=True, null=True)
    bio = models.TextField(verbose_name='ひとこと', max_length=100, blank=True, null=True)
    instrument = models.ForeignKey(Part, verbose_name='パート', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'CustomUser'

    def __str__(self):
        return self.name
