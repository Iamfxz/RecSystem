# Generated by Django 2.1 on 2020-03-01 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userbrowse'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=64, verbose_name='用户ID')),
                ('tag', models.CharField(blank=True, max_length=64, verbose_name='用户标签')),
            ],
            options={
                'verbose_name_plural': '用户标签',
                'db_table': 'UserTag',
            },
        ),
    ]
