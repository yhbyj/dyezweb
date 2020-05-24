# Generated by Django 2.2 on 2020-05-23 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('three_competitions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threecompetitionrule',
            name='status',
        ),
        migrations.AlterField(
            model_name='threecompetitionrule',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='三项竞赛评分细则描述'),
        ),
        migrations.AlterField(
            model_name='threecompetitionrulecategory',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='类别描述'),
        ),
    ]
