# Generated by Django 5.0.6 on 2024-05-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='index',
            name='algorithm',
            field=models.CharField(default='e', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='index',
            unique_together={('term', 'document', 'algorithm')},
        ),
        migrations.AddIndex(
            model_name='index',
            index=models.Index(fields=['term', 'document', 'algorithm'], name='Search_inde_term_55dad1_idx'),
        ),
    ]