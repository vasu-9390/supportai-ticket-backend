from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'role', 'profile_image', 'created_at')
        read_only_fields = ('id', 'created_at')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    fullName = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'fullName', 'email', 'password', 'role')
        extra_kwargs = {'name': {'required': False}}

    def validate(self, attrs):
        if 'fullName' in attrs and not attrs.get('name'):
            attrs['name'] = attrs.pop('fullName')
        elif 'name' not in attrs:
            attrs['name'] = attrs.get('email', '').split('@')[0]
        return attrs

    def create(self, validated_data):
        validated_data.pop('fullName', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data.get('name', 'User'),
            password=validated_data['password'],
            role=validated_data.get('role', 'Agent')
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)
        return {
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
