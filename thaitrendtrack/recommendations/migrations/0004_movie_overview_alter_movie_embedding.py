# Generated by Django 4.1.2 on 2025-03-09 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0003_movie_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='embedding',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
