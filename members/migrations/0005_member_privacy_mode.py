# Generated by Django 4.1.1 on 2022-09-25 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_member_facebook_url_member_instagram_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='privacy_mode',
            field=models.BooleanField(default=False, verbose_name='privacy_mode'),
        ),
    ]
