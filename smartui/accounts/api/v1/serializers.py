from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from smartui.utils import (
    otp_utils,
    email_utils,
    constants
)
from django.utils import timezone
from smartui.accounts.models import OTP
from django.db.models import Q
from smartui.medicals.models import ExternalProviders
import random as rd
# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str
# from mimi.accounts.mails.tokens import account_activation_token
# from smartui.accounts.mails import account_activation

User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "image",
            "username",
            "email",
            "password",
            "date_of_birth",
            "role",
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        if ("username" not in validated_data) or ('provider_name' not in validated_data):
            validated_data["username"] = (
                f"{validated_data['first_name']} {validated_data['last_name']} {rd.randint(3, 1000)}"
            )

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()

        return user

        
        """
            Activating account
        """
        # NOTE: THE COMMENTED LINE OF CODE BELOW WILL BE UNCOMMENTED, AFTER OLADISEA'S  TEST

        # current_site_domain = self.context["request"].META['HTTP_HOST']
        # account_activation.send_activation_email(user,current_site_domain)




# # class ActivateAccountSerializer(serializers.Serializer):
# #     def validate(self, attrs):
# #         user_id = force_str(urlsafe_base64_decode(self.context["uid"]))
# #         token = self.context["token"]

# #         user = User.objects.filter(id=user_id).first()
# #         if user is None:
# #             raise serializers.ValidationError("user doesn't exist")
# #         if account_activation_token.check_token(user, token) is False:
# #             raise serializers.ValidationError("wrong token or token expired")

# #         elif user is not None and account_activation_token.check_token(user, token):
# #             user.is_active = True
# #             user.save()
# #             attrs["message"] = "Account Activated"
# #             return attrs

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id","first_name", "last_name", "address", "image", "role", "username"]


class IntialSignInSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])
            ).first()
        generated_otp = otp_utils.generate_otp()
        
        if user is None or user.is_active == False:
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "user doesn't exist or inactive account"
            })
        
        if user and (user.check_password(attrs["password"]) == False):
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "Invalid Password"
            })

        if user and user.check_password(attrs["password"]):
            full_name = f"{user.first_name} {user.last_name}"
            email_utils.sign_in_with_otp_activation_mail(
                user.email,
                full_name,
                generated_otp,
            )
            
            obj, created = OTP.objects.get_or_create(
               user=user,
                defaults={
                    'otp': generated_otp
                }
            )
            if obj:
                obj.otp = generated_otp
                obj.time_created = timezone.now()
                obj.save()
            attrs["username"] = user.username
            return attrs
    
    def to_representation(self, attrs):
        attrs.pop('password')
        attrs["error"] = "false"
        return attrs

class FinalSignInSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    otp = serializers.CharField(min_length=6)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])
            ).first()
        user_otp = OTP.objects.filter(user=user, 
                                       otp=attrs["otp"]).first()     
        if (user is None):
            raise serializers.ValidationError(
                {
                    "error": "true",
                    "message": "user doesn't exist"
                }
            )
        
        if (user and user_otp is None):
             """
                user exists and token expired
             """
             raise serializers.ValidationError({
                    "message": "invalid otp or token expired" 
                })
        
        if(user and user_otp):
            user_otp = OTP.objects.filter(user=user, 
                                       otp=attrs["otp"]).first()
            period_of_user_otp = (timezone.now() - user_otp.time_created).total_seconds()
            
            if (period_of_user_otp >= constants.OTP_TIMEOUT) :
                raise serializers.ValidationError({
                    "error": "true",
                    "message": "invalid otp or token expired " 
                })        
            
            if(period_of_user_otp < constants.OTP_TIMEOUT):
                OTP.objects.get(
                    user=user, 
                    otp=attrs["otp"]).delete()
                return user
          
    def to_representation(self, instance):
        user = User.objects.get(email=instance.email)
        refresh = RefreshToken.for_user(instance)
        return {
            "Info": f"Welcome {instance.username}", 
            "access_token": str(refresh.access_token),
            "user": ProfileSerializer(instance).data,
            }



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        """
        This is for validating the values the user provides in order to nge their password
        """
        user = self.context["request"].user

        if user.check_password(attrs["old_password"]) is False:
            raise serializers.ValidationError(
                {"status": "false", "message": "Please provide the old password"}
            )

        elif attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "status": "false",
                    "message": "new password not same as confirm password",
                }
            )

        elif user.check_password(attrs["new_password"]):
            raise serializers.ValidationError(
                {
                    "status": "false",
                    "message": "new password can't be same as old password",
                }
            )

        elif (attrs["old_password"] != attrs["new_password"]) and (
            attrs["new_password"] == attrs["confirm_password"]
        ):
            attrs["status"] = "true"
            return attrs



class OtpResetPaswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        user_email = User.objects.filter(email=attrs["email"]).first()

        if user_email is None:
            raise serializers.ValidationError(
                {
                    "status": "false",
                    "message": "email address is invalid or don't exist",
                }
            )



