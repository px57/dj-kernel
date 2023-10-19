# Generated by Django 4.2 on 2023-10-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text="The object's creation date/time", null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now_add=True, help_text="The object's last update date/time", null=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['-updated_on'],
                'get_latest_by': 'updated_on',
                'abstract': False,
            },
        ),
    ]
