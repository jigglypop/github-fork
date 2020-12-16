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


# 프로필 검색
class ProfileSearchViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = ProfileSearchSerializer
    pagination_class = LargeResultsSetPagination


    def list(self,request,*args,**kwargs):
        if request.GET.get('nickname'):
            nickname =  request.GET.get('nickname')
            queryset = list(Profile.objects.filter(
                nickname__icontains=nickname).values('user','user_image','nickname','permission',))[:5]
            return JsonResponse(queryset,safe=False)
        else:
            return JsonResponse({})


# 프로필 확인
class ProfileConfirmViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = ProfileSerializer

    def list(self,request,*args,**kwargs):
        if request.GET.get('username'):
            username =  request.GET.get('username')
            queryset = list(Profile.objects.filter(
                username=username).values('username'))[:5]
            if queryset:
                return JsonResponse({'results':1},safe=False)
            else:
                return JsonResponse({'results':0},safe=False)
        if request.GET.get('email'):
            email =  request.GET.get('email')
            queryset = list(Profile.objects.filter(
                email=email))
            if queryset:
                return JsonResponse({'results':1},safe=False)
            else:
                return JsonResponse({'results':0},safe=False)
        else:
            return JsonResponse({})


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# 프로필 차일드셋
class ProfilePostViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, pk=pk)
        if profile:
            like = list(profile.myposts.values('id','title'))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                like_pagination = Paginator(like,5)
                like_page = list(like_pagination.get_page(page))
                like_count = like_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > like_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if like_count != 1:
                        nexts = f'/api/profilelike/{pk}/?page=2'
                else:
                    if page == str(like_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/profilelike/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/profilelike/{pk_str}/?page={page_str_next}'
                        previous = f'/api/profilelike/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':like_page,'count':like_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(like)
        

class ProfileLikeViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, pk=pk)
        if profile:
            like = list(profile.posts.values('id','title'))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                like_pagination = Paginator(like,5)
                like_page = list(like_pagination.get_page(page))
                like_count = like_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > like_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if like_count != 1:
                        nexts = f'/api/profilelike/{pk}/?page=2'
                else:
                    if page == str(like_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/profilelike/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/profilelike/{pk_str}/?page={page_str_next}'
                        previous = f'/api/profilelike/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':like_page,'count':like_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(like)


# 이메일로 찾기 
class ProfileEmailViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileEmailSerializer

    # 이메일로 찾기
    def list(self, request,*args,**kwargs):
        if request.GET.get('email'):
            email =  request.GET.get('email')
            queryset = list(Profile.objects.filter(
                email=email))
            if queryset:
                return JsonResponse({'results':'success'},safe=False)
            else:
                return JsonResponse({'results':'fail'},safe=False)
        else:
            return JsonResponse({})


# 미니 프로필


class MiniProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = MiniProfileSerializer

# 리스트 프로필

class ListProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ListProfileSerializer
    pagination_class = LargeResultsSetPagination

