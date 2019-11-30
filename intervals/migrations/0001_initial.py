# Generated by Django 2.2.7 on 2019-11-27 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('interval', models.CharField(max_length=30)),
                ('guess', models.CharField(max_length=30)),
                ('audio_url', models.URLField()),
                ('is_correct', models.IntegerField(default=0)),
            ],
        ),
    ]
