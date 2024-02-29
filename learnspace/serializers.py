from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, Lesson, Group, UserProductAccess


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Помимо основных полей модели, сериализатор отображает следующую
    вычисляемую информацию о продукте:
    - lessons_count: Количество уроков, связанных с продуктом.
    - students_count: Количество учеников, занимающихся на продукте.
    - groups_fill_percentage: Средний процент заполненности всех групп
    продукта.
    - product_purchase_percentage: Процент пользователей, которые приобрели
    продукт относительно общего числа пользователей на платформе.
    """
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    product_purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'start_datetime',
            'cost', 'lessons_count', 'creator',
            'min_users', 'max_users', 'slug',
            'students_count', 'groups_fill_percentage',
            'product_purchase_percentage'
        ]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с продуктом."""
        return Lesson.objects.filter(product=obj).count()

    def get_students_count(self, obj):
        """Возвращает количество учеников, занимающихся на продукте."""
        return UserProductAccess.objects.filter(product=obj).count()

    def get_groups_fill_percentage(self, obj):
        """
        Возвращает процент заполненности групп. Рассчитывается как отношение
        общего числа учеников в группах к общей вместимости всех групп.
        """
        groups = obj.associated_groups.all()
        total_capacity = obj.max_users * groups.count() if groups else 0
        total_students = sum(group.users.count() for group in groups)
        fill_percentage = (
                    total_students / total_capacity * 100
        ) if total_capacity else 0
        return round(fill_percentage, 2)

    def get_product_purchase_percentage(self, obj):
        """
        Возвращает процент приобретения продукта. Рассчитывается как
        отношение числа пользователей с доступом к продукту к общему числу
        пользователей на платформе.
        """
        total_accesses = UserProductAccess.objects.filter(product=obj).count()
        total_users = User.objects.filter(is_superuser=False).count()
        return round(
            (total_accesses / total_users * 100) if total_users else 0, 2
        )


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Предоставляет информацию о конкретном уроке, включая идентификатор,
    название и URL видео.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url']


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Предоставляет информацию о группе, включая идентификатор, название,
    продукт, к которому относится группа, и список участников группы.
    """
    class Meta:
        model = Group
        fields = ['id', 'name', 'product', 'users']
