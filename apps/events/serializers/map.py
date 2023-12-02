from rest_framework import serializers


class GeoJsonSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)
    crs = serializers.DictField(
    )
    features = serializers.ListField(
        child=serializers.DictField(
        )
    )
