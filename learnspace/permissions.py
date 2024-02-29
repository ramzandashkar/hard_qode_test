from rest_framework import permissions

from .models import UserProductAccess


class HasProductAccess(permissions.BasePermission):
    """
    Пользовательский permission для проверки доступа пользователя к продукту.
    """

    def has_permission(self, request, view):
        product_id = view.kwargs.get('product_id')
        user = request.user
        # Проверяем, имеет ли пользователь доступ к продукту
        if product_id and user.is_authenticated:
            return UserProductAccess.objects.filter(
                user=user,
                product__id=product_id).exists()
        return False
