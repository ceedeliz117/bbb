from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def check_stock(sender, instance, **kwargs):
    if instance.stock < 10:
        logger.warning(f"Stock for product '{instance.name}' is below 10. Current stock: {instance.stock}")
