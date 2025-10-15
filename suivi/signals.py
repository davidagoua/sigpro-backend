from django.db.models.signals import post_save
from django.dispatch import receiver

from prsep.settings.base import pusher_client
from .models import TDR
from core.redis_service import get_redis_service


redis_service = get_redis_service()


@receiver(post_save, sender=TDR)
def notify_tdr_change(sender, instance: TDR, created, **kwargs):
    """
    Signal qui s'exécute après la création ou la modification d'un objet TDR
    """

    data = {
            'id': instance.pk,
            'action': 'created' if created else 'updated',
            # Ajoutez d'autres champs selon vos besoins
        }

    # Émission de l'événement
    channel = 'tdr-changes'
    event = 'tdr-create' if created else 'tdr-change'
    pusher_client.trigger(channel, event, data)
    redis_service.add_notifications(instance.user.pk, data)


