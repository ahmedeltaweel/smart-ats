from rest_framework import permissions

# make sure user is a registered user in listing GET
# make sure user is company admin in creation.
# make sure user is company admin and i linked to company on update and delete.


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(request.user, "companyadmin"):
            return False
        # check for action if create return True
        if request.method == "POST" and not obj:
            return True
        # update, delete
        return request.user.companyadmin in obj.company_admin.all()
