from games.Serializers.GameSerializer import GameSerializer
from shared.Serializer import BaseSerializer
from users.UserSerializer import UserSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'user': UserSerializer(instance.user, request=self.request).serialize(),
            'key': instance.status_order(),
            'price': instance.price,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
        }
