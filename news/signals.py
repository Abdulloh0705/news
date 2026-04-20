from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .utils import send_to_telegram


@receiver(post_save, sender=News)
def send_news_to_telegram(sender, instance, created, **kwargs):
    if created and instance.status == "published":
        send_to_telegram(instance)
