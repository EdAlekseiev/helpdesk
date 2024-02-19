# Generated by Django 5.0.2 on 2024-02-18 19:48

from django.db import migrations

from users.utils import constants


def add_permissions_for_operator(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)

    view_request = Permission.objects.get(codename="view_request")
    change_request = Permission.objects.get(codename="view_request")

    operator_group.permissions.add(view_request, change_request)

def add_permissions_for_client(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    operator_group = Group.objects.get(name=constants.CLIENT_GROUP_NAME)

    view_request = Permission.objects.get(codename="view_request")
    change_request = Permission.objects.get(codename="view_request")
    add_request = Permission.objects.get(codename="add_request")

    operator_group.permissions.add(add_request, view_request, change_request)


class Migration(migrations.Migration):

    dependencies = [
        ("requests", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_permissions_for_operator),
        migrations.RunPython(add_permissions_for_client),
    ]
