# Generated by Django 4.2.4 on 2023-08-10 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_user_unique_together_pupil'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pupil',
            old_name='group',
            new_name='groups',
        ),
    ]
