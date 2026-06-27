from django.shortcuts import render
from django.urls import resolve
from django.core.exceptions import PermissionDenied

class RoleCheckingMiddleware:
    """
    Middleware that checks if a user is trying to access a view
    belonging to another role.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path_info
            
            # Simple check based on URL paths
            if path.startswith('/customer/') and not request.user.is_customer() and not request.user.is_admin():
                # Mechanics can't access /customer/ routes
                return render(request, 'errors/403.html', {'message': 'Mechanic accounts cannot access the Customer portal.'}, status=403)
                
            if path.startswith('/mechanic/') and not request.user.is_mechanic() and not request.user.is_admin():
                # Customers can't access /mechanic/ routes
                return render(request, 'errors/403.html', {'message': 'Customer accounts cannot access the Mechanic portal.'}, status=403)

        response = self.get_response(request)
        return response
