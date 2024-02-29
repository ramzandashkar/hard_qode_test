from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Product, UserProductAccess, Lesson, Group


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'cost', 'start_datetime',
        'creator', 'min_users', 'max_users',
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'creator__username',)
    list_filter = ('start_datetime', 'creator',)
    ordering = ('start_datetime',)


@admin.register(UserProductAccess)
class UserProductAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'access_granted')
    search_fields = ('user__username', 'product__name',)
    list_filter = ('access_granted',)
    ordering = ('access_granted',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'video_url')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'product__name',)
    list_filter = ('product',)
    ordering = ('product', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'product__name',)
    list_filter = ('product',)
    ordering = ('name',)
    filter_horizontal = ('users',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'users':
            kwargs['widget'] = FilteredSelectMultiple("users",
                                                      is_stacked=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
