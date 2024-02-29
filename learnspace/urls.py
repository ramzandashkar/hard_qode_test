from django.urls import path
from .views import ProductListView, LessonListView, GroupListView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path(
        'products/<int:product_id>/lessons/',
        LessonListView.as_view(),
        name='lesson-list'
    ),
    path(
        'products/<int:product_id>/groups/',
        GroupListView.as_view(),
        name='group-list'
    ),
]
