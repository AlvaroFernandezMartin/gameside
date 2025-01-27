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
            'category': str(instance.category) if instance.category else None,
            'platforms': [str(platform) for platform in instance.platforms.all()]
            if hasattr(instance.platforms, 'all')
            else instance.platforms,
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
            'released_at': instance.released_at.isoformat()
            if isinstance(instance.released_at, datetime)
            else None,
            'pegi': instance.pegi,
            'category': str(instance.category) if instance.category else None,
            'platforms': [str(platform) for platform in instance.platforms.all()]
            if hasattr(instance.platforms, 'all')
            else instance.platforms,
        }
