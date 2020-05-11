from django.db import models


class Provider(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    name = models.CharField(
        verbose_name="Наименование поставщика", max_length=256, unique=True
    )

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    UNITS = (
        (1, "kg"),
        (2, "lb"),
        (3, "pcs"),
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Поставщик"
    )

    name = models.CharField(verbose_name="Наименование товара", max_length=256)
    created_at = models.DateTimeField(
        verbose_name="Дата поступления", auto_now_add=True
    )
    price = models.DecimalField(
        verbose_name="Цена за единицу товара", max_digits=19, decimal_places=4
    )
    unit = models.PositiveSmallIntegerField(
        verbose_name="Единица измерения", choices=UNITS
    )
