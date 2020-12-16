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



# 포스트
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    )
    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post:
            post.numlike = len(list(post.profiles.values()))
            post.numcomment = len(list(post.comments.values()))
            post.viewcount += 1
            post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        post_data = request.data
        if post_data['category'] == 'gallery':
            if post_data['image_file']:
                image_data = post_data['image_file']
                format, imgstr = image_data.split(';base64,')
                imgdata = base64.b64decode(imgstr)
                ext = format.split('/')[-1]
                # 파일 경로
                file_url = 'image'+datetime.today().strftime("%Y%m%d%H%M%S")+ '.' + ext 
                post_data['image_file'] = ContentFile(imgdata, name=file_url)
            else:
                post_data['image_file'] = None
        else:
            post_data['image_file'] = None
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 포스트 검색
class PostSearchViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSearchSerializer
    pagination_class = LargeResultsSetPagination

    def list(self,request,*args,**kwargs):
        if request.GET.get('category') and request.GET.get('title'):
            category =  request.GET.get('category')
            title = request.GET.get('title')
            queryset = list(Post.objects.filter(
                title__icontains=title,
                category__icontains=category).values('id','title'))[:5]
            return JsonResponse(queryset,safe=False)
        else:
            return JsonResponse({})




# 메인 리스트
class MainListViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = MainListSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args,**kwages):
        data = json.loads(request.body.decode('utf-8'))
        category_set = []
        for category in data['category']:
            post = Post.objects.filter(category=category).order_by('-created_at')
            postlist=list(post.values())


            # 프로필 닉네임, 이미지 넣기
            for post in postlist:
                profileid = post['profileid_id']
                profilequery = Profile.objects.all()
                profile_post = get_object_or_404(profilequery,pk=profileid)
                post['user_image'] = profile_post.user_image
                post['nickname'] = profile_post.nickname
                post['permission'] = profile_post.permission

            # 페이지 갯수 조절
            profile_list_pagination = Paginator(postlist,5)
            profile_page = list(profile_list_pagination.get_page(1))
            category_set.append([{'category':category,'results':profile_page}][0])
        return JsonResponse(category_set, safe=False)


# 포스트 라이크
class PostLikeViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post:
            postprofile = list(post.profiles.values('user','username','nickname','user_image','permission',))
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                profile_list_pagination = Paginator(postprofile,10)
                profile_page = list(profile_list_pagination.get_page(page))
                profile_count = profile_list_pagination.num_pages
                nexts = None
                previous = None
                pk_str = str(pk)
                if int(page) > profile_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if profile_count != 1:
                        nexts = f'/api/postlike/{pk}/?page=2'
                else:
                    if page == str(profile_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/postlike/{pk_str}/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/postlike/{pk_str}/?page={page_str_next}'
                        previous = f'/api/postlike/{pk_str}/?page={page_str_pre}'
                return JsonResponse({'results':profile_page,'count':profile_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(postprofile)

# 갤러리
class GalleryViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = MiniListSerializer

    def list(self, request,*args,**kwargs):
        post = Post.objects.filter(category='gallery').order_by('-created_at')
        postlist = list(post.values())[:5]
        return JsonResponse({'results':postlist}, safe=False)



# 미니 리스트
class MiniListViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = MiniListSerializer
    # pagination_class = LargeResultsSetPagination

    def list(self, request,*args,**kwargs):
        post = Post.objects.all().order_by('-created_at')
        category = ""
        if request.GET.get('category'):
            post = Post.objects.filter(category=request.GET.get('category')).order_by('-created_at')
            postlist = list(post)
            if len(postlist) == 0:
                return JsonResponse({'results':[],'count':0,'next':None,'previous':None}, safe=False)
            category=f"&category={request.GET.get('category')}"
        if post:
            postcategory = list(post.values())
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                post_list_pagination = Paginator(postcategory,10)
                post_page = list(post_list_pagination.get_page(page))
                post_count = post_list_pagination.num_pages

                # 프로필 닉네임, 이미지, 권한 넣기
                for post in post_page:
                    profileid = post['profileid_id']
                    profilequery = Profile.objects.all()
                    profile_post = get_object_or_404(profilequery,pk=profileid)
                    post['user_image'] = profile_post.user_image
                    post['nickname'] = profile_post.nickname
                    post['permission'] = profile_post.permission

                nexts = None
                previous = None
                if int(page) > post_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if post_count != 1:
                        nexts = f'/api/minilist/?page=2'+ category
                else:
                    if page == str(post_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/minilist/?page={page_str}'+ category
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/minilist/?page={page_str_next}'+ category
                        previous = f'/api/minilist/?page={page_str_pre}'+ category
                return JsonResponse({'results':post_page,'count':post_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(postcategory)



# 미니 갤러리
class MiniGalleryViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = MiniListSerializer

    def list(self, request,*args,**kwargs):
        post = Post.objects.filter(category="gallery").order_by('-numlike','-created_at')
        if post:
            postcategory = list(post.values())
            page = request.GET.get('page')
            if page:
                # 여기 페이지 수 조절할것
                post_list_pagination = Paginator(postcategory,10)
                post_page_temp = list(post_list_pagination.get_page(page))
                post_count = post_list_pagination.num_pages
                post_page = []
                # src로 바꾸기
                # 서버 s3_url
                s3_url = 'https://languagetogetherimage.s3.ap-northeast-2.amazonaws.com/media/'
                for post in post_page_temp:
                    post_temp = {}
                    for itme in post:
                        post_temp['src'] = s3_url + post['image_file'] 
                        post_temp['width'] = post['width']
                        post_temp['height'] = post['height']
                        post_temp['id'] = post['id']
                        post_temp['title'] = post['title']
                        post_temp['created_at'] = post['created_at']
                        post_temp['viewcount'] = post['viewcount']
                        post_temp['numlike'] = post['numlike']
                        post_temp['numcomment'] = post['numcomment']
                    post_page.append(post_temp)

                nexts = None
                previous = None
                if int(page) > post_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if post_count != 1:
                        nexts = f'/api/minigallery/?page=2'
                else:
                    if page == str(post_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/minigallery/?page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/minigallery/?page={page_str_next}'
                        previous = f'/api/minigallery/?page={page_str_pre}'
                return JsonResponse({'results':post_page,'count':post_count,'next':nexts,'previous':previous}, safe=False)
            else:
                return Response(postcategory)


class NoticeViewset(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    pagination_class = LargeResultsSetPagination

class LoadMorePosts(generics.ListAPIView):
    serializer_class = PostSerializer