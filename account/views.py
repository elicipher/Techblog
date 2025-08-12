from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import (
    EmailSerializer ,
    OTPSerializer , 
    InitialProfileSerializer , 
    CompleteProfileSerializer)

from .models import OtpCode , User
import random
from permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

 
# Create your views here.
class SendOtpCodeView(APIView):
    """

        (SendOtpCodeView) : To Send OTP Code for login/register user
    
    """
    permission_classes = [IsNotAuthenticated,]
    serializer_class = EmailSerializer
    def post(self , request):
        srz_data = self.serializer_class(data= request.data)
        if srz_data.is_valid():
            email = srz_data.validated_data['email']
            random_code = random.randint(10000 , 99999)
            OtpCode.objects.filter(email = email).delete()
            OtpCode.objects.create(email = email , code =  random_code)
            print('OTP code :',random_code)
            return Response({"status":"code sent"}, status= status.HTTP_201_CREATED)
        return Response(srz_data.errors , status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    """
    (VerifyCodeView): Verifies the OTP code sent to user's email

    """
    permission_classes = [IsNotAuthenticated,]
    serializer_class = OTPSerializer
    def post(self , request):
        srz_data = self.serializer_class(data= request.data)
        if srz_data.is_valid():
            email = srz_data.validated_data['email']
            code = srz_data.validated_data['code']

            try :
                code_instance = OtpCode.objects.get(code = code , email = email)
            except OtpCode.DoesNotExist :
                return Response({"status":"Code not found . try again"},status=status.HTTP_404_NOT_FOUND)
            
            if code_instance.check_and_delete_if_expired():
                code_instance.delete()
                return Response({"status":"Code expired. try again."} , status=status.HTTP_408_REQUEST_TIMEOUT)
            
            if code_instance.code != code :
                return Response({"status":"The code entered is incorrect."} , status= status.HTTP_400_BAD_REQUEST)
            
                        # ساخت یا دریافت یوزر
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'full_name': f"user-{uuid.uuid4().hex[:8]}"}
            )

            refresh = RefreshToken.for_user(user)
            if created:
                return Response({
                    "status": "new user",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "logged in",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)

        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
                        
class CompleteProfileView(APIView):
    """

    (CompleteProfileView) : Complete regiteration and choice interest tag
    
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = InitialProfileSerializer
    def post(self , request):
        srz_data = self.serializer_class(instance=request.user,data = request.data ,partial = True)
        if srz_data.is_valid():
            srz_data.save()
            return Response({"staus":"profile compcompleted ." },status=status.HTTP_200_OK)
        return Response(srz_data.errors , status= status.HTTP_400_BAD_REQUEST)


class EditProfileView(APIView):
    """
    (EditProfileView) : Edit Profile

    """

    permission_classes = [IsAuthenticated,]
    serializer_class = CompleteProfileSerializer
    def patch(self , request):
        srz_data = self.serializer_class(instance=request.user,data = request.data , partial = True)
        if srz_data.is_valid():
            srz_data.save()
            return Response({"staus":"profile changed ."},status=status.HTTP_200_OK)
        return Response(srz_data.errors , status= status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """

    (Logout View ) : block refresh token and logout
    
    """
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try :
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
