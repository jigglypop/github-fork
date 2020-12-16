from django.shortcuts import render
from .serializers import PostSerializer, RegisterUserSerializer, UserSerializer, LoginUserSerializer, LargeResultsSetPagination
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import viewsets
from .serializers import PostSerializer,PostLikeSerializer, ProfileSerializer
from .serializers import MiniProfileSerializer,MiniListSerializer,ListProfileSerializer
from .serializers import EventSerializer,EventJoinSerializer

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




# 이벤트
class EventViewset(viewsets.ModelViewSet):
    now = datetime.now()
    queryset = Event.objects.filter(start__gte=now).order_by('-created_at')
    serializer_class = EventSerializer


# 이벤트 5개
class EventFiveViewset(viewsets.ModelViewSet):
    now = datetime.now()
    queryset = Event.objects.filter(start__gte=now).order_by('start')[:5]
    serializer_class = EventSerializer

# 이벤트 조인
class EventJoinViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventJoinSerializer

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        if event:
            eventprofile = list(event.profile.values('user','username','nickname','user_image','permission',))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                profile_list_pagination = Paginator(eventprofile,10)
                profile_page = list(profile_list_pagination.get_page(page))
                profile_count = profile_list_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > profile_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if profile_count != 1:
                        nexts = f'/api/eventjoin/{pk}/?page=2'
                else:
                    if page == str(profile_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/eventjoin/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/eventjoin/{pk_str}/?page={page_str_next}'
                        previous = f'/api/eventjoin/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':profile_page,'count':profile_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(eventprofile)

