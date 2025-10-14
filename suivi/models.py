from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from core.models import Departement, Exercice
from planification.models import Tache, Drf
from programme.models import Activite, TacheProgram
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



User = get_user_model()


class CommentaireTDR(TimeStampedModel,models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    tdr = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()


class TDR(TimeStampedModel,models.Model):
    file = models.FileField(verbose_name='Fichier', upload_to='tdr')
    exercice=models.ForeignKey(Exercice, on_delete=models.SET_NULL, null=True, blank=True)
    file_final = models.FileField(verbose_name="TDR fin d'activité", upload_to='tdr', null=True, blank=True)
    label = models.TextField(null=True, blank=True)
    departemnt = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.IntegerField(default=0)
    activity = models.ForeignKey(Tache, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Activité")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comments = GenericRelation(CommentaireTDR)
    lessons = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    injonction = models.BooleanField(default=False)
    accorder = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.label} - {self.state}'

    @property
    def has_comments(self):
        return self.comments.exists()



class TDRProgramme(TimeStampedModel,models.Model):
    file = models.FileField(verbose_name='Fichier', upload_to='tdr', blank=False)
    file_final = models.FileField(verbose_name="TDR fin d'activité", upload_to='tdr', null=True, blank=True)
    label = models.TextField(null=True, blank=True)
    state = models.IntegerField(default=0)
    activity = models.ForeignKey(Activite, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Activité")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comments = GenericRelation(CommentaireTDR)
    lessons = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    injonction = models.BooleanField(default=False)
    accorder = models.BooleanField(default=False)

    @property
    def has_comments(self):
        return self.comments.exists()

    def __str__(self):
        return f'{self.label} - {self.state}'



@receiver(models.signals.post_save, sender=TDR)
def tdr_post_save(sender, instance, created, **kwargs):
    if not created:
        try:
            channel_layer = get_channel_layer()
            channel_name = f'tdr_{instance.id}'
            async_to_sync(channel_layer.group_send)(
                channel_name,
                {
                    'type': 'tdr_update',
                    'data': {
                        'id': instance.id,
                        'state': instance.state
                    }
                }
            )
        except Exception as e:
            print(e)



        
        