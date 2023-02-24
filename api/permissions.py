from rest_framework import permissions


class ExpiringLinkPermission(permissions.BasePermission):
    message = 'Update your tier.'

    def has_permission(self, request, view):

        return request.user.account.tier.expiring_link