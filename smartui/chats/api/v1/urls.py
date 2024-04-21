from django.urls import path
from smartui.chats.api.v1.views import (
    EditOrDeleteMessagesAPIView,
    MessageAPIView,
    GenerateUniqueIDForChatAPIView,
)

app_name = "chats"

urlpatterns = [
    path(
        "edit-or-delete-messages/<uuid:room_name>/",
        EditOrDeleteMessagesAPIView.as_view(),
        name="edit_or_delete_messages",
    ),
    
    path(
        "get-message/<uuid:other_user_id>/",
        MessageAPIView.as_view(),
        name="get_message",
    ),

    path('generate-chat-id/', 
         GenerateUniqueIDForChatAPIView.as_view(), 
         name='generate_chat_id'
    ),
]
