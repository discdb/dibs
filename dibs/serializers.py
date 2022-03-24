from rest_framework.serializers import ModelSerializer

from .models import ImageModel

class ImageSerializer(ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'

