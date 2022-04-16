from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipe.models import Recipe
from .models import Profile
from recipe.serializers import RecipeSerializer
from . import serializers

User = get_user_model()


class UserRegistrationAPIView(GenericAPIView):
    """endpoint  регистрации нового пользователя"""
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    """endpoint авторизации"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validate_data
        serializer = serializers.CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            'refresh': str(token),
            'access': str(token.access_token)
        }


class UserLogoutAPIView(GenericAPIView):
    """endpoint выхода"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    """изменение пользовательских данных """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user


class UserProfileAPIView(RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class UserAvatarAPIView(RetrieveUpdateAPIView):
    """изменение фото пользователя"""
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class UserBookmarkAPIView(ListCreateAPIView):
    """Get, Create, Delete избранных рецептов"""
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
    profile = Profile.objects.all()

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        user_profile = get_object_or_404(self.profile, user=user)
        return user_profile.bookmarks.all()

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        user_profile = get_object_or_404(self.profile, user=user)
        recipe = Recipe.objects.get(id=request.data['id'])
        if user_profile:
            user_profile.bookmarks.add(recipe)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        user_profile = get_object_or_404(self.profile, user=user)
        recipe = Recipe.objects.get(self.request.data['id'])
        if user_profile:
            user_profile.bookmarks.delete(recipe)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPIView(UserAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer

    def get_object(self):
        return self.request.user






