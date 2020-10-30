# Generated by Django 3.1.2 on 2020-10-30 07:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Joined')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('license_type', models.CharField(choices=[('free', 'Free'), ('trial', 'Trial'), ('pro', 'Professional'), ('enterprise', 'Enterprise')], default='free', max_length=15, verbose_name='License Type')),
                ('name', models.CharField(default='Free', max_length=50, verbose_name='License Name')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='License Price')),
                ('duration', models.DurationField(blank=True, verbose_name='License Duration')),
            ],
            options={
                'verbose_name': 'License',
                'verbose_name_plural': 'Licenses',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.customuser')),
                ('phone_no', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Invalid Phone Number', regex='^\\+(?:[0-9] ?){6,14}[0-9]$')])),
                ('org_name', models.CharField(blank=True, max_length=255, verbose_name='Organization')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('bank_name', models.CharField(blank=True, max_length=512, verbose_name='Associated Bank Name')),
                ('bank_acc', models.CharField(blank=True, max_length=24, verbose_name='Bank Account No')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='LoginEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Login Timestamop')),
                ('ip_address', models.GenericIPAddressField(verbose_name='Clients IP address')),
                ('ip_address_type', models.CharField(max_length=50, verbose_name='Type of IP address')),
                ('user_agent', models.CharField(max_length=255, verbose_name='Clients User Agent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Login Entry',
                'verbose_name_plural': 'Login Entries',
            },
        ),
        migrations.CreateModel(
            name='UserLicense',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.customuser')),
                ('current_license_qt', models.PositiveIntegerField(default=1, verbose_name='Current License Quantity')),
                ('current_license_price', models.PositiveIntegerField(default=0, verbose_name='Current License Price')),
                ('iat', models.DateTimeField(auto_now=True, verbose_name='License Issued at')),
                ('eat', models.DateTimeField(auto_now_add=True, verbose_name='License Expires at')),
                ('total_price', models.PositiveIntegerField(default=0, verbose_name='Total Price')),
                ('applied_license', models.CharField(blank=True, choices=[('free', 'Free'), ('trial', 'Trial'), ('pro', 'Professional'), ('enterprise', 'Enterprise')], max_length=10, verbose_name='Applied for')),
                ('applied_license_qt', models.PositiveIntegerField(default=0, verbose_name='Applied License Quantity')),
                ('upgradingfrom_license', models.CharField(blank=True, choices=[('free', 'Free'), ('trial', 'Trial'), ('pro', 'Professional'), ('enterprise', 'Enterprise')], max_length=10, verbose_name='Upgrading from')),
                ('assigned_license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='accounts.license', verbose_name='Assigned License')),
            ],
            options={
                'verbose_name': 'User License',
                'verbose_name_plural': 'User Licenses',
            },
        ),
    ]
