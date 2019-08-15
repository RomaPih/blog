# Generated by Django 2.2.4 on 2019-08-15 09:35

from django.db import migrations, models
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='email адреса')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='phone number')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name="ім'я")),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='прізвище')),
                ('is_staff', models.BooleanField(default=False, verbose_name='статус персоналу')),
                ('is_active', models.BooleanField(default=True, verbose_name='активний')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата приєднання')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'користувач',
                'verbose_name_plural': 'користувачі',
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]