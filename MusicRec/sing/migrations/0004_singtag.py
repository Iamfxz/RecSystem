# Generated by Django 2.1 on 2020-03-01 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sing', '0003_sing'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sing_id', models.CharField(max_length=64, unique=True, verbose_name='歌手ID')),
                ('tag', models.CharField(blank=True, max_length=64, verbose_name='歌手标签')),
            ],
            options={
                'verbose_name_plural': '歌手标签',
                'db_table': 'SingTag',
            },
        ),
    ]
