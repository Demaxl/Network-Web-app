# Generated by Django 4.2.7 on 2023-11-27 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_follow_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('following', 'follower')},
        ),
    ]
