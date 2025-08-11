from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

def get_tag_queryset():
    from blog.models import Tag
    return Tag.objects.all()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()


class InitialProfileSerializer(serializers.ModelSerializer):

    interest = serializers.PrimaryKeyRelatedField(queryset=get_tag_queryset(),many=True)

    class Meta:
        model = User
        fields = ['full_name','interest',]
        extra_kwargs = {
            'full_name': {'required': True},
            'interest' : {'required': False},
        }

class CompleteProfileSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ['avatar','full_name','email']
            extra_kwargs = {
                'full_name': {'required': True},
                'email' : {'required': False},
            }
    

     