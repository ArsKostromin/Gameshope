from rest_framework import permissions

class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем создание только администраторам и суперпользователям
        return request.user and (request.user.is_staff or request.user.is_superuser)
