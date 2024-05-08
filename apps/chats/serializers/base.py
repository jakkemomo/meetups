from rest_framework import serializers


class SendingBaseSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj) -> str:
        if obj.created_by:
            return obj.created_by.image_url
        # TODO: Needs an image for system notifications
        return ""
