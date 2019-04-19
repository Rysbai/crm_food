# Generated by Django 2.1.5 on 2019-04-19 02:39

from django.db import migrations


def add_admin_role(apps, schema_editor):
    Role = apps.get_model('app', 'Role')

    role = Role.objects.create(name='Admin')
    role.save()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_auto_20190416_1142'),
    ]

    operations = [
        migrations.RunPython(add_admin_role),
    ]
