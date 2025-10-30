from rest_framework import serializers

from core.models import Exercice


class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = ['id','label']