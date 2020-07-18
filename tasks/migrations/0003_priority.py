# Generated by Django 2.2.10 on 2020-07-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20200712_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_count', models.PositiveIntegerField(default=0)),
                ('medium_count', models.PositiveIntegerField(default=0)),
                ('low_count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
