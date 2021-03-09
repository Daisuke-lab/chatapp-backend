# Generated by Django 3.1.1 on 2020-12-15 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Swipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL)),
                ('swiped', models.ManyToManyField(blank=True, related_name='swiped', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='swipe', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('age', models.CharField(blank=True, max_length=3, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('native_lan', models.CharField(max_length=20)),
                ('foreign_lan', models.CharField(max_length=20)),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('time_start', models.TimeField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('intro', models.TextField(blank=True, null=True)),
                ('freeday', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='../images/')),
                ('default', models.BooleanField(default=False)),
                ('width', models.FloatField(default=100, null=True)),
                ('length', models.FloatField(default=100, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Profile.profile')),
            ],
        ),
    ]