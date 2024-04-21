from smartui.chats.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username")
    receiver = serializers.CharField(source="receiver.username")

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "edit_count", "message"]


class EditOrDeleteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["edit_count", "message"]

    def update(self, instance, validated_data):
        instance.edit_count += 1
        return super().update(instance, validated_data)
