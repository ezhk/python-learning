from django.db import models


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'

    name = models.CharField(verbose_name='name of category', max_length=68, unique=True)
    description = models.CharField(verbose_name='description of category', max_length=128)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.description})"


class Products(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='name of product', max_length=64)
    short_description = models.CharField(verbose_name='short comment of product', max_length=512)
    full_description = models.TextField(verbose_name='large protuct description', blank=True)
    overview = models.TextField(verbose_name='large product review', blank=True)
    image_preview = models.ImageField(upload_to='product-img', blank=True, default='product-img/blank-product.svg')
    price = models.DecimalField(verbose_name='product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='stock quantity', default=0)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.category.name}, {self.price})"


class Properties(models.Model):
    class Meta:
        verbose_name = 'Product property'
        verbose_name_plural = 'Product properties'

    name = models.CharField(verbose_name='property', max_length=128, unique=True)

    def __str__(self):
        return f"{self.name}"


class ProductAndProperty(models.Model):
    class Meta:
        verbose_name = 'Product and property (link)'
        verbose_name_plural = 'Products and properties (links)'

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}, {self.property.name}"


class FeedBack(models.Model):
    username = models.CharField(verbose_name='Имя пользователя', max_length=64, blank=True, null=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=128)

    subject = models.CharField(verbose_name='Тема', max_length=64, blank=True, null=True)
    body = models.CharField(verbose_name='Сообщение', max_length=1024)

    def __str__(self):
        return f"{self.email} ({self.subject})"
