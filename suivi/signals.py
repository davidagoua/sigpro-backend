from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TDR
import pusher
import json
from django.conf import settings



try:
    pusher_client = pusher.Pusher(
        app_id='app-id',
        key='app-key',
        secret='app-secret',
        host='sigpro-mena.com',  # Par exemple: 'localhost'
        port=6001,  # Port par défaut de Soketi
        ssl=False  # Selon votre configuration
    )



    @receiver(post_save, sender=TDR)
    def notify_tdr_change(sender, instance, created, **kwargs):
        """
        Signal qui s'exécute après la création ou la modification d'un objet TDR
        """

        data = {
                'id': instance.id,
                'action': 'created' if created else 'updated',
                # Ajoutez d'autres champs selon vos besoins
            }

        # Émission de l'événement
        channel = 'tdr-changes'
        event = 'tdr-create' if created else 'tdr-change'
        pusher_client.trigger(channel, event, data)

except:
    pusher_client = None