# Generated by Django 5.2.1 on 2025-05-27 06:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0006_alter_manga_translation_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('chapter_number',), 'verbose_name': 'Bob', 'verbose_name_plural': 'Boblar'},
        ),
        migrations.AddField(
            model_name='chapter',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='chapter_pdfs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='PDF boblari'),
        ),
    ]
