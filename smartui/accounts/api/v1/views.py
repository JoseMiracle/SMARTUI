from rest_framework import generics, permissions, status
from smartui.accounts.api.v1.serializers import (
    RegistrationSerializer,
    IntialSignInSerializer,
    FinalSignInSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    OtpResetPaswordSerializer,
)


from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class IntialSignInAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = IntialSignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)



class FinalSignInAPIView(generics.GenericAPIView):
    """
        This is for 2FA
    """
    serializer_class = FinalSignInSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
    
class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            user.set_password(serializer.validated_data["confirm_password"])
            user.save()
            return Response({"message": "password changed"}, status=status.HTTP_200_OK)


class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class OtpForResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = OtpResetPaswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "password changed"}, status=status.HTTP_200_OK)
