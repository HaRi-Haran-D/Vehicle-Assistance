from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def customer_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a customer,
    raising PermissionDenied if not.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def mechanic_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a mechanic,
    raising PermissionDenied if not.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_mechanic(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
