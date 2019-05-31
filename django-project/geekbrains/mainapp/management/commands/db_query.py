from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Case, When, F, DecimalField, Q, Sum, ExpressionWrapper
from django.utils.timezone import now

from geekbrains import settings
from orderapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        CALCULATE_VALUES = {
            0: {
                'discount': 10,
                'created_after': timedelta(hours=12),
            },
            1: {
                'discount': 5,
                'created_after': timedelta(days=1),
            },
            2: {
                'discount': 3,
                'created_after': timedelta(days=7),
            }
        }

        for idx, desc in CALCULATE_VALUES.items():
            CALCULATE_VALUES[idx].update(
                {'condition': Q(order__created__gte=now() - desc['created_after'])})

        order_discount = OrderItem.objects.annotate(
            discount=Case(
                *(
                    When(desc['condition'],
                         then=desc['discount']) for idx, desc in CALCULATE_VALUES.items()
                ),
                output_field=DecimalField()
            ),
            total_price=Case(
                *(
                    When(desc['condition'],
                         then=F('product__price') * F('quantity') * (1 - desc['discount'] / 100.0))
                    for idx, desc in CALCULATE_VALUES.items()
                ),
                output_field=DecimalField()
            ),
            item_price=ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        ).filter(
            ~Q(total_price=None) & ~Q(discount=None)
        ).order_by(
            'order_id', 'total_price'
        ).select_related()

        print("Описание позиций заказов:")
        for items in order_discount:
            print("\t", ', '.join([f"номер заказа: {items.order_id}",
                                   f"артикул продукта: {items.product_id}",
                                   f"скидка: {items.discount}%",
                                   f"цена без скидки: {items.item_price}",
                                   f"итоговая сумма со скидкой: {items.total_price}"]))

        print("Пересчитанные заказы:")
        for order in order_discount.order_by('order_id').values('order_id').annotate(summary_price=Sum('total_price')):
            print(f"\t{order}")
        print("Общая сумма заказов со скидками:", order_discount.aggregate(Sum('total_price')).get('total_price__sum'))

        if settings.DEBUG:
            from django.db import connection
            print("\nSQL запросы:")
            for q in connection.queries:
                print('\t', q.get('sql'))
