# Generated by Django 2.2 on 2019-04-24 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='imagesAndTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgId', models.CharField(max_length=200)),
                ('tag1', models.CharField(max_length=200)),
            ],
        ),
    ]
