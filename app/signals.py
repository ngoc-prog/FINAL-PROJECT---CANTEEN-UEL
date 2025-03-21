from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order, OrderItem

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if instance.complete and created:
        # Update product sales count when order is completed
        for item in instance.orderitem_set.all():
            item.product.sales_count += item.quantity
            item.product.save()

@receiver(post_save, sender=OrderItem)
def orderitem_post_save(sender, instance, created, **kwargs):
    # Update order total when items change
    instance.order.save()