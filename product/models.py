from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


# Tag Model
class Tag(models.Model):
    tag = models.CharField(max_length=100, default='')
    tag_slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        base_slug = slugify(self.tag if not self.tag_slug else self.tag_slug)
        slug = base_slug
        num = 1
        while Tag.objects.filter(tag_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        self.tag_slug = slug
        super().save(*args, **kwargs)


# Brand Model
class Brand(models.Model):
    brand = models.CharField(max_length=100, default='')
    brand_slug = models.SlugField(max_length=100, unique=True, blank=True)
    brand_image = models.ImageField(upload_to='brand_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        base_slug = slugify(self.brand if not self.brand_slug else self.brand_slug)
        slug = base_slug
        num = 1
        while Brand.objects.filter(brand_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        self.brand_slug = slug
        super().save(*args, **kwargs)


# Category Model
class Category(models.Model):
    category = models.CharField(max_length=100, default='Men')
    category_slug = models.SlugField(max_length=100, unique=True, blank=True)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        base_slug = slugify(self.category if not self.category_slug else self.category_slug)
        slug = base_slug
        count = 1
        while Category.objects.filter(category_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        self.category_slug = slug
        super().save(*args, **kwargs)


# Variation Model
class Variation(models.Model):
    name = models.CharField(max_length=100, default='')
    value = models.CharField(max_length=100, default='')
    variation_slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.value}"


# Product Model
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=200, unique=True, blank=True, null=True)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(blank=True, null=True)

    has_variation = models.BooleanField(default=False, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        base_slug = slugify(self.product_name if not self.product_slug else self.product_slug)
        slug = base_slug
        num = 1
        while Product.objects.filter(product_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        self.product_slug = slug
        super().save(*args, **kwargs)


# ProductVariation Model
class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_variations'
    )
    variation = models.ForeignKey(
        Variation,
        on_delete=models.SET_NULL,   # safer than CASCADE
        null=True,
        blank=True
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'variation')

    def __str__(self):
        return f"{self.product} - {self.variation}"
