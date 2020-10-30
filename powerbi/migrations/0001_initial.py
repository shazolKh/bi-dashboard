# Generated by Django 3.1.2 on 2020-10-30 07:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Dashboard Name')),
                ('dashboard_id', models.CharField(max_length=250, unique=True, verbose_name='Dashboard ID')),
                ('thumbnail_url', models.CharField(max_length=250, verbose_name='Thumbnail URL')),
                ('license_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.license', verbose_name='License Type')),
            ],
            options={
                'verbose_name': 'dashboard',
                'verbose_name_plural': 'dashboards',
            },
        ),
    ]
