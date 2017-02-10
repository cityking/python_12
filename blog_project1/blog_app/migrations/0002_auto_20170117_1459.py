# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='\u5e7f\u544a\u6807\u9898')),
                ('description', models.CharField(max_length=200, verbose_name='\u5e7f\u544a\u63cf\u8ff0')),
                ('image_url', models.ImageField(upload_to='ad/%Y/%m', verbose_name='\u56fe\u7247\u8def\u5f84')),
                ('callback_url', models.URLField(blank=True, null=True, verbose_name='\u56de\u8c03url')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('index', models.IntegerField(default=999, verbose_name='\u6392\u5217\u987a\u5e8f')),
            ],
            options={
                'ordering': ['index', 'id'],
                'verbose_name': '\u5e7f\u544a',
                'verbose_name_plural': '\u5e7f\u544a',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('desc', models.CharField(max_length=50, verbose_name='\u6587\u7ae0\u63cf\u8ff0')),
                ('content', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('click_count', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6b21\u6570')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63a8\u8350')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-date_publish'],
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u5206\u7c7b\u540d\u79f0')),
                ('index', models.IntegerField(default=999, verbose_name='\u5206\u7c7b\u6392\u5e8f')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('username', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7528\u6237\u540d')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='\u90ae\u7bb1\u5730\u5740')),
                ('url', models.URLField(blank=True, max_length=100, null=True, verbose_name='\u4e2a\u4eba\u7f51\u9875\u5730\u5740')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_app.Article', verbose_name='\u6587\u7ae0')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_app.Comment', verbose_name='\u7236\u7ea7\u8bc4\u8bba')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'ordering': ['-date_publish'],
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='\u6807\u9898')),
                ('description', models.CharField(max_length=200, verbose_name='\u53cb\u60c5\u94fe\u63a5\u63cf\u8ff0')),
                ('callback_url', models.URLField(verbose_name='url\u94fe\u63a5\u5730\u5740')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('index', models.IntegerField(default=999, verbose_name='\u6392\u5217\u987a\u5e8f')),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': '\u53cb\u60c5\u94fe\u63a5',
                'verbose_name_plural': '\u53cb\u60c5\u94fe\u63a5',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u6807\u7b7e\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_app.Category', verbose_name='\u5206\u7c7b'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='blog_app.Tag', verbose_name='\u6807\u7b7e'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]