# Generated by Django 3.0 on 2020-09-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_follow_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cover_photo',
            field=models.FileField(blank=True, default='/image/default/default_cover_photo.png', null=True, upload_to='image/users/cover_photo/', verbose_name='cover_photo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.FileField(blank=True, default='/image/default/default_profile_photo.png', null=True, upload_to='image/users/profile_photo/', verbose_name='profile_photo'),
        ),
    ]
