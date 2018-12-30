# Generated by Django 2.1.4 on 2018-12-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photoName', models.CharField(max_length=50)),
                ('distinguishType', models.IntegerField(default=1)),
                ('path', models.CharField(max_length=100)),
                ('postDate', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
