from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    message = "شما قبلا وارد شده اید اجازه ورود به این صفحه را ندارید."

    def has_permission(self, request, view):
        return not request.user.is_authenticated