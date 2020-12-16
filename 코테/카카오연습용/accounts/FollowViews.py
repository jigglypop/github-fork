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



# 팔로워
class FollowerViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class =FollowerSerializer

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        follower = get_object_or_404(queryset, pk=pk)
        if follower:
            followerprofile = list(follower.follower.values('user','username','nickname','user_image','permission',))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                profile_list_pagination = Paginator(followerprofile,10)
                profile_page = list(profile_list_pagination.get_page(page))
                profile_count = profile_list_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > profile_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if profile_count != 1:
                        nexts = f'/api/follower/{pk}/?page=2'
                else:
                    if page == str(profile_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/follower/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/follower/{pk_str}/?page={page_str_next}'
                        previous = f'/api/follower/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':profile_page,'count':profile_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(followerprofile)


# 팔로잉
class FollowingViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class =FollowingSerializer

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        following = get_object_or_404(queryset, pk=pk)
        if following:
            followingprofile = list(following.following.values('user','username','nickname','user_image','permission',))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                profile_list_pagination = Paginator(followingprofile,10)
                profile_page = list(profile_list_pagination.get_page(page))
                profile_count = profile_list_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > profile_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if profile_count != 1:
                        nexts = f'/api/following/{pk}/?page=2'
                else:
                    if page == str(profile_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/following/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/following/{pk_str}/?page={page_str_next}'
                        previous = f'/api/following/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':profile_page,'count':profile_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(followingprofile)

