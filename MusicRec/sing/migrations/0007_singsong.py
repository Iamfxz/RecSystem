# Generated by Django 2.1 on 2020-04-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0008_song'),
        ('sing', '0006_singsim'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sing_id', models.CharField(blank=True, max_length=64, verbose_name='歌手ID')),
                ('song_id', models.ForeignKey(on_delete=models.DO_NOTHING, related_name='歌曲信息', to='song.Song')),
            ],
            options={
                'verbose_name_plural': '歌手的歌曲',
                'db_table': 'SingSong',
            },
        ),
    ]
