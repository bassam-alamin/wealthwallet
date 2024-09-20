from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from apps.auth_app.models import User
from apps.auth_app.serializers import MetroAuthTokenSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (UserRateThrottle,)
    serializer_class = MetroAuthTokenSerializer

    @swagger_auto_schema(
        request_body=MetroAuthTokenSerializer,
        responses={200: openapi.Response('Success', MetroAuthTokenSerializer),
                   400: 'Bad Request'},
    )
    def post(self, request, format=None):
        serializer = MetroAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        request.user = user
        return super(LoginView, self).post(request, format=None)

    def get_context(self, **kwargs):
        context = super(LoginView, self).get_context()
        context['title'] = 'Login'
        context['description'] = 'Login to your account'
        return context


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']

    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, id=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=id)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
