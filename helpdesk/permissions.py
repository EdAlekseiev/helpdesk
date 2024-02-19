from rest_framework.permissions import (
    DjangoModelPermissions as BaseDjangoModelPermissions
)


class DjangoModelPermissions(BaseDjangoModelPermissions):
    perms_map = {
        **BaseDjangoModelPermissions.perms_map,
        **{
            "GET": ["%(app_label)s.view_%(model_name)s"]
        },
    }
