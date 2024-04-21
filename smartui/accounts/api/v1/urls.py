from django.urls import path
from smartui.accounts.api.v1.views import (
    RegistrationAPIView,    
    ChangePasswordAPIView,
    UpdateProfileAPIView,
    UserProfileAPIView,
    IntialSignInAPIView,
    FinalSignInAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path('initial-sign-in/', IntialSignInAPIView.as_view(), name='initial_sign_in'),
    path('final-sign-in/', FinalSignInAPIView.as_view(), name='final_sign_in'),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("update-profile/", UpdateProfileAPIView.as_view(), name="update_profile"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
]
