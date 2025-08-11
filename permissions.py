from rest_framework.permissions import BasePermission , SAFE_METHODS


class IsNotAuthenticated(BasePermission):
    message = "شما قبلا وارد شده اید اجازه ورود به این صفحه را ندارید."

    def has_permission(self, request, view):
        return not request.user.is_authenticated
    

class IsOwnerOrReadOnly(BasePermission):
    message = "Permission denied: you are not the owner."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated 

    
    def has_object_permission(self, request, view, obj):
        # if request is "GET , OPTIONS , HEAD" : return True becouse user want read 
        if request.method in SAFE_METHODS :
            return True
        # else : if request user want change obj should be owner 
        return obj.author == request.user