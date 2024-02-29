from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Product(models.Model):
    name = models.CharField(max_length=settings.MAX_LENGTH_MODELS_FIELD)
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_MODELS_FIELD,
        unique=True,
        blank=True,
    )
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_products',
    )
    min_users = models.IntegerField()
    max_users = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProductAccess(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_accesses',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='user_access_records',
    )
    access_granted = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'User Product Access'
        verbose_name_plural = 'User Product Accesses'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Lesson(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    name = models.CharField(max_length=settings.MAX_LENGTH_MODELS_FIELD)
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_MODELS_FIELD,
        unique=True,
        blank=True,
    )
    video_url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='associated_groups',
    )
    name = models.CharField(max_length=settings.MAX_LENGTH_MODELS_FIELD)
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_MODELS_FIELD,
        unique=True,
        blank=True,
    )
    users = models.ManyToManyField(User, related_name='learnspace_groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
