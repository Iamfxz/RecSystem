# Generated by Django 2.1 on 2020-02-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.CharField(max_length=64, unique=True, verbose_name='用户ID')),
                ('u_name', models.CharField(max_length=150, verbose_name='用户昵称')),
                ('u_birthday', models.DateField(blank=True, verbose_name='生日')),
                ('u_gender', models.IntegerField(blank=True, verbose_name='用户性别')),
                ('u_province', models.CharField(blank=True, max_length=20, verbose_name='用户省份')),
                ('u_city', models.CharField(blank=True, max_length=20, verbose_name='用户城市')),
                ('u_type', models.CharField(blank=True, max_length=10, verbose_name='用户类型')),
                ('u_tags', models.CharField(blank=True, max_length=1000, verbose_name='用户标签')),
                ('u_img_url', models.CharField(blank=True, max_length=1000, verbose_name='头像链接')),
                ('u_auth_status', models.CharField(blank=True, max_length=10, verbose_name='用户状态')),
                ('u_account_status', models.CharField(blank=True, max_length=10, verbose_name='账号状态')),
                ('u_dj_status', models.CharField(blank=True, max_length=10, verbose_name='DJ状态')),
                ('u_vip_type', models.CharField(blank=True, max_length=10, verbose_name='VIP状态')),
                ('u_sign', models.TextField(blank=True, verbose_name='用户签名')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'db_table': 'User',
            },
        ),
    ]
