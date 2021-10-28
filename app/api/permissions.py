from rest_framework import permissions


class IsAlbumOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        print('You can\'t view this album ')
        return False
