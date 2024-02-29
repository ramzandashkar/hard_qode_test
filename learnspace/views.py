from rest_framework import generics

from .models import Product, Lesson, Group
from .permissions import HasProductAccess
from .serializers import ProductSerializer, LessonSerializer, GroupSerializer


class ProductListView(generics.ListAPIView):
    """
    Представление для получения списка всех продуктов.

    Возвращает список всех продуктов на платформе, включая
    дополнительную информацию, такую как количество уроков, количество
    учеников, процент заполнения групп и процент приобретения продукта.
    Никакие разрешения для доступа не требуются.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonListView(generics.ListAPIView):
    """
    Представление для получения списка уроков, связанных с конкретным
    продуктом.

    Доступ к этому представлению ограничен и требует наличия доступа к
    соответствующему продукту. URL запроса должен включать идентификатор
    продукта ('product_id') для фильтрации уроков. Использует
    пользовательское разрешение 'HasProductAccess' для проверки доступа
    пользователя.
    """
    serializer_class = LessonSerializer
    permission_classes = [HasProductAccess]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(product__id=product_id)


class GroupListView(generics.ListAPIView):
    """
    Представление для получения списка групп, связанных с конкретным продуктом.

    URL запроса должен включать идентификатор продукта ('product_id') для
    фильтрации групп. Предоставляет список всех групп, привязанных к
    указанному продукту. Если 'product_id' не предоставлен, возвращает
    пустой список групп.
    """
    serializer_class = GroupSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id is not None:
            return Group.objects.filter(product__id=product_id)
        else:
            return Group.objects.none()
