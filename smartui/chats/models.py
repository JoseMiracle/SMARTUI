from django.db import models
from django.contrib.auth import get_user_model
from smartui.utils.base_class import BaseModel

User = get_user_model()


class ChatIDs(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_chats")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_chats")

class Message(BaseModel):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name="sender_mesages",
        null=True,
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name="receiver_messages",
        null=True,
    )
    edit_count = models.IntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return self.message
    
"""
    VERSION CONTROL SYSTEM
"""

