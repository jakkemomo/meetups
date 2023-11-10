from rest_framework import serializers

from apps.events.models import Tag


class TagCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = Tag
        fields = ["id", "name"]

    def create(self, validated_data):
        name = validated_data.pop("name")
        tag_object = Tag.objects.create(name=name)
        return tag_object


class TagRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TagUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = Tag
        fields = ["id", "name"]

    def update(self, instance, validated_data):
        name = validated_data.pop("name")
        instance.name = name
        instance.save()
        return instance


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
