from accounts.models import CustomUser
from django.db import models
import datetime


class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='作成者', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='練習名', max_length=20)
    location = models.CharField(verbose_name='練習場所', max_length=40, blank=True, null=True)
    detail = models.TextField(verbose_name='練習内容', blank=True, null=True)
    date = models.DateField(verbose_name='練習日', default=datetime.date.today())
    start_at = models.TimeField(verbose_name='開始時刻', default=datetime.datetime.today())
    end_at = models.TimeField(verbose_name='終了時刻', default=datetime.datetime.today())
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Schedule'

    def __str__(self):
        return self.title


class Reaction(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='回答者', on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, verbose_name='練習予定', on_delete=models.CASCADE)
    state = models.CharField(verbose_name='回答', max_length=5)
    comment = models.TextField(verbose_name='コメント', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Reaction'

    def __str__(self):
        return self.state