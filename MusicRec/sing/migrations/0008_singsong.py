# Generated by Django 2.1 on 2020-04-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sing', '0007_singsong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singsong',
            name='sing_id',
            field=models.CharField(max_length=64, verbose_name='歌手ID'),
        ),
        migrations.AlterField(
            model_name='singsong',
            name='song_id',
            field=models.CharField(max_length=64, verbose_name='歌曲ID'),
        ),
    ]
