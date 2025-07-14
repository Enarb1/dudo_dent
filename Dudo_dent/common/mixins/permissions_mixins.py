from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class BaseRolePermissionMixin(UserPassesTestMixin):
    """Base MixIn for role permissions.
    Adding the allowed roles and checking if the user has permission.
    Default 403 error handling"""
    allowed_roles = []

    def has_required_role(self, user):
        return user.is_staff or any(getattr(user,f"is_{role.lower()}", False) for role in self.allowed_roles)

    def handle_no_permission(self):
        return redirect('https://http.dog/403.jpg')


class RoleRequiredMixin(BaseRolePermissionMixin):
    """Check if the user has the required role/s."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and self.has_required_role(user)


class OwnerAndRolePermissionMixin(BaseRolePermissionMixin):
    """Check if the user has the required role/s or if he is the owner."""
    def test_func(self):
        user_to_view = self.get_object()
        current_user = self.request.user

        return (
                current_user.is_authenticated and
                (current_user == user_to_view or
                 self.has_required_role(current_user)
                 ))
