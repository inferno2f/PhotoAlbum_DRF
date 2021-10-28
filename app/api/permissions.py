from rest_framework import permissions


class IsAlbumOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.is_superuser:
            return True
        print('You can\'t view this album ')
        return False
