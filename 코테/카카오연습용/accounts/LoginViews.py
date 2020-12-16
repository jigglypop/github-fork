from django.shortcuts import render
from .serializers import PostSerializer, RegisterUserSerializer, UserSerializer, LoginUserSerializer, LargeResultsSetPagination
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import viewsets
from .serializers import PostSerializer,PostLikeSerializer, ProfileSerializer
from .serializers import MiniProfileSerializer,MiniListSerializer,ListProfileSerializer
from .serializers import NoticeSerializer, EventSerializer,EventJoinSerializer
from .serializers import RecommentSerializer,  CommentSerializer
from .serializers import FollowerSerializer,  FollowingSerializer
from .serializers import ProfileEmailSerializer
from .serializers import MainListSerializer
from .serializers import PostSearchSerializer,ProfileSearchSerializer
from .models import Post,  Profile
from .models import Notice,  Event
from .models import Comment, Recomment
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from pprint import pprint
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
import requests
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime
from django.http import HttpResponse
# 이미지 업로드용
import boto3
import uuid
from PIL import Image
from io import BytesIO




class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
