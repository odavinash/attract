# Generated by Django 2.0.2 on 2019-04-10 12:17

from django.db import migrations, models
import lunchorderingapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('lunchorderingapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depreciation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_path', models.FileField(blank=True, default='', help_text='excel file', upload_to=lunchorderingapp.models.get_upload_import_path)),
            ],
            options={
                'db_table': 'import_user',
            },
        ),
    ]
