from datetime import datetime

from shared.Serializer import BaseSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url) if instance.cover else None,
            'stock': instance.stock,
            'released_at': instance.released_at.isoformat()
            if isinstance(instance.released_at, datetime)
            else None,
            'pegi': instance.pegi,
            'category': BaseSerializer.serialize(instance.category),
            'platforms': BaseSerializer.serialize(instance.category),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url) if instance.cover else None,
            'stock': instance.stock,
            'created_at': instance.created_at.isoformat()
            if isinstance(instance.created_at, datetime)
            else None,
            'updated_at': instance.updated_at.isoformat()
            if isinstance(instance.updated_at, datetime)
            else None,
        }
