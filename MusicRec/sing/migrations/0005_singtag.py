# Generated by Django 2.1 on 2020-03-01 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sing', '0004_singtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singtag',
            name='sing_id',
            field=models.CharField(max_length=64, verbose_name='歌手ID'),
        ),
    ]
