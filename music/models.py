from django.db import models
from accounts.models import CustomUser

class Music(models.Model):
    category_choice = ((1, '前'), (2, '中'), (3, 'メイン'), (4, 'その他'))
    class Meta:
        db_table = 'music'
        ordering = ['end_date',]
        verbose_name = verbose_name_plural = '曲'
    
    title = models.CharField(verbose_name='曲名(正式名称)', max_length=40)
    short_title = models.CharField(verbose_name='曲名(略称)', max_length=20)
    start_date = models.DateField(verbose_name='練習開始日')
    end_date = models.DateField(verbose_name='練習終了日')
    category = models.IntegerField(choices=category_choice)

    def __str__(self):
        return self.title

class Stage(models.Model):
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='回答者', on_delete=models.CASCADE)
    state = models.CharField(verbose_name='パート', max_length=5)
    comment = models.TextField(verbose_name='コメント', max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Stage'

