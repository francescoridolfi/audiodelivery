# Generated by Django 5.0.6 on 2024-05-18 19:05

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioChunk',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Edited At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0, help_text='Chunk Ordering Number assigned by system while uploading', verbose_name='Order N.')),
                ('start_time', models.TimeField(help_text='Start time of the audio chunk', verbose_name='Start Time')),
                ('end_time', models.TimeField(help_text='End time of the audio chunk', verbose_name='End Time')),
                ('file_path', models.FilePathField(help_text='Path where the file is stored', max_length=255, verbose_name='File path')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_editor_related', to=settings.AUTH_USER_MODEL, verbose_name='Edited By')),
            ],
            options={
                'verbose_name': 'Audio Chunk',
                'verbose_name_plural': 'Audio Chunks',
            },
        ),
    ]