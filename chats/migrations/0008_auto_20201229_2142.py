# Generated by Django 3.1.1 on 2020-12-29 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0007_auto_20201229_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='file',
            new_name='chat_file',
        ),
        migrations.AlterField(
            model_name='file',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='chats.contact'),
        ),
    ]
