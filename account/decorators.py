from rest_framework import permissions
from utils.constants import UserType

login_required = permissions.IsAuthenticated
super_admin_required = permissions.IsAdminUser


class teacher_required(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type == UserType.TEACHER


class student_required(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type == UserType.STUDENT


class secretary_required(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type == UserType.SECRETARY
