# Generated by Django 3.0.6 on 2020-07-01 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='ひとこと'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nick_name',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='表示名'),
        ),
    ]
