# Generated by Django 4.1.6 on 2023-02-12 09:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_dislike_quantity_post_dislikes_post_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_posts', through='api.DisLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked_posts', through='api.Like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('liked_user', 'liked_post')},
        ),
    ]