from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from smartui.chats.models import Message, ChatIDs
from smartui.chats.api.v1.serializers import (
    EditOrDeleteMessageSerializer,
    MessageSerializer,
)

from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()



class EditOrDeleteMessagesAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditOrDeleteMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def get_object(self):
        message_obj = Message.objects.get(id=self.kwargs["message_id"])
        return message_obj

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class MessageAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        condition_1 = Q(receiver=self.kwargs["other_user_id"], sender=self.request.user)
        condition_2 = Q(sender=self.kwargs["other_user_id"], receiver=self.request.user)
        message_queryset = Message.objects.filter(condition_1 | condition_2).all()

        return message_queryset

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GenerateUniqueIDForChatAPIView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        sender = self.request.data['sender']
        receiver = self.request.data['receiver']
        
       

         
        condition_1 = Q(receiver=receiver, sender=receiver)
        condition_2 = Q(sender=sender, receiver=receiver)
        chat_details = ChatIDs.objects.filter(
            condition_1 | condition_2
        ).first()

        if chat_details is not None:
            print(ChatIDs.objects.count())
            print(chat_details.id)
            return Response (
                data={"chat_id": 
                      chat_details.id},
                status=status.HTTP_200_OK
            )

        if chat_details is None:
            chat_detail = ChatIDs.objects.create(sender_id=sender, receiver_id=receiver)
            print(ChatIDs.objects.count())
            return Response (
                data={"chat_id": chat_detail.id
                      
                    },
                status=status.HTTP_200_OK
            )

        
