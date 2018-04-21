# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-21 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=260)),
                ('favorites_count', models.IntegerField()),
                ('retweets_count', models.IntegerField()),
                ('replies_count', models.IntegerField()),
                ('date_created', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('handle', models.CharField(max_length=50, unique=True)),
                ('followers_count', models.IntegerField()),
                ('all_tweets_count', models.IntegerField()),
                ('following_count', models.IntegerField()),
                ('likes_count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataFetcher.User'),
        ),
    ]