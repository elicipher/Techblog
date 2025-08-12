from django.urls import path
from . import views

urlpatterns = [

    path("send-otp-code/",views.SendOtpCodeView.as_view()),
    path("verify-code/",views.VerifyCodeView.as_view()),
    path("complete-profile/",views.CompleteProfileView.as_view()),
    path("edit-profile/",views.EditProfileView.as_view()),
    path("log_out/",views.LogoutView.as_view())
    
]
