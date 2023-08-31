from .models import Utilisateurs
from rest_framework import serializers


class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'
