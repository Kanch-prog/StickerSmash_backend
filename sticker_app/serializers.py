from rest_framework import serializers
from .models import Sticker

# Sticker Serializer to handle Sticker model data
class StickerSerializer(serializers.ModelSerializer):
    # Custom field to represent the username instead of the full user object
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Sticker
        fields = [
            'id',                # Sticker ID
            'image',             # Image associated with the sticker
            'uploaded_at',       # Upload time of the sticker
            'description',       # Description of the sticker
            'category',          # Category of the sticker
            'ward',
            'latitude',          # Latitude for location
            'longitude',         # Longitude for location
            'priority',          # Priority of the sticker
            'status',            # Current status of the sticker
            'user',              # User who uploaded the sticker (now represented by username)
        ]
        extra_kwargs = {
            'user': {'read_only': True},  # User is read-only (admin or system assigned)
        }
