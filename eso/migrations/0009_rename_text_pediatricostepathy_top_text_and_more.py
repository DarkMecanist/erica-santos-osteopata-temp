# Generated by Django 4.0.1 on 2022-02-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eso', '0008_pediatricostepathy_pediatricostepathyreasons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pediatricostepathy',
            old_name='text',
            new_name='top_text',
        ),
        migrations.AddField(
            model_name='pediatricostepathy',
            name='bottom_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
