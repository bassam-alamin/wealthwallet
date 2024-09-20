from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


User = get_user_model()


class MetroAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    exclude_fields = ['password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        credentials = {
            'email': email,
            'password': password
        }

        user_obj = User.objects.filter(email=email).first()
        attrs = self.validate_user_details(user_obj, credentials, attrs)
        return attrs

    def validate_user_details(self, user_obj, credentials, attrs):
        if user_obj is not None:

            if all(credentials.values()):
                user = authenticate(request=self.context.get('request'), **credentials)

                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Must include "email" and "password".')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    email_verified_message = serializers.SerializerMethodField(
        label=_("Email Verified Message"),
        read_only=True
    )
    password_last_updated_message = serializers.SerializerMethodField(
        label=_("Password Last Updated Message"),
        read_only=True
    )
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        exclude = ('created_at', 'updated_at', 'last_login', 'is_deleted',
                   'created_by', 'updated_by', 'is_test')
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'email_verified_message': {'read_only': True}
        }

    def get_email_verified_message(self, obj):
        if not obj.email_verified:
            return 'Email is not verified'
        return 'Email is verified'

    def get_password_last_updated_message(self, obj):
        if obj.password_last_updated:
            days = (timezone.now() - obj.password_last_updated).days
            if days > 90:
                return 'Password has not been updated for more than 90 days. Please update your password.'
            return "Password upto date"
        return 'Password has never been set'

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                _("Password must be at least 8 characters long.")
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("User with this email already exists.")
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                _("User with this username already exists.")
            )
        return value

    def validate(self, data):
        if data.get('email'):
            self.validate_email(data['email'])
        if data.get('password'):
            self.validate_password(data['password'])
        if data.get('username'):
            self.validate_username(data['username'])
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user