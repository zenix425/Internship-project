from rest_framework import serializers
from account.models import User
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email','name', 'password','password2']
        extra_kwargs = {
            'password': {'write_only':True},
            'password2': {'write_only':True}
        }

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        print("password:", password)
        print("password2:", password2)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Remove password2 from validated_data
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user =self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password don't match")
        user.set_password(password)
        user.save()
        return attrs