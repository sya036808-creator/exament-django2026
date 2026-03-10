from rest_framework import serializers
from .models import CustomUser

# Sérialiseur pour afficher et gérer les détails complets de l'utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Champs exposés par l'API
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'avatar']
        # L'identifiant et le rôle ne doivent pas être modifiés directement
        read_only_fields = ['id', 'role']

# Sérialiseur public pour afficher les informations de base de l'utilisateur
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Champs exposés publiquement
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'role']
