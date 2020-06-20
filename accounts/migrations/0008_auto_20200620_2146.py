# Generated by Django 3.0 on 2020-06-20 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200620_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ConnectionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('accepted', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_received', to='accounts.UserProfile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_sent', to='accounts.UserProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
