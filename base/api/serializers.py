from rest_framework.serializers import ModelSerializer
from base.models import Room

# turn Python object into JSON


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  # serialize all fields from Room model
