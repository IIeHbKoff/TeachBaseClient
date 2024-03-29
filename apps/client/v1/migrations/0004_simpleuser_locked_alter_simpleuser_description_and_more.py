# Generated by Django 4.2.3 on 2023-07-10 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_alter_course_authors_alter_course_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleuser',
            name='locked',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='external_id',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='last_activity_at',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='simpleuser',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
