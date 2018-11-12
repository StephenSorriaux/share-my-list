# Generated by Django 2.1.3 on 2018-11-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_choice_is_bought_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='link_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='list',
            name='total_cost',
            field=models.FloatField(default=0),
        ),
    ]