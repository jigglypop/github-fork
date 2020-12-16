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


# 코멘트 리코멘트

class RecommentViewset(viewsets.ModelViewSet):
    queryset = Recomment.objects.all()
    serializer_class = RecommentSerializer

    def list(self,request):
        queryset = Recomment.objects.all().order_by('-created_at')
        serializer_class = RecommentSerializer
        comment_id = request.GET.get('comment')
        if comment_id:
            queryset = Comment.objects.all()
            commentparents = get_object_or_404(queryset, pk=comment_id)
            recommentpost = list(commentparents.recomments.values().order_by('-created_at'))
            page = request.GET.get('page')
            if page:
               # 여기 페이지 수 조절할것
                recomment_list_pagination = Paginator(recommentpost,5)
                recomment_page = list(recomment_list_pagination.get_page(page))
                # 프로필 이미지 넣기
                if len(recomment_page) != 0:
                    recomment_temp = []
                    for recomment_item in recomment_page:
                        recomment_id = recomment_item['commenter']
                        profile_query = Profile.objects.all()
                        recommenter = get_object_or_404(profile_query, pk=recomment_id)
                        # commenter_value = list(commenter)
                        recomment_item['user_image'] = recommenter.user_image
                        recomment_item['nickname'] = recommenter.nickname
                        recomment_item['permission'] = recommenter.permission

                # 프로필 뽑기 전처리
                recomment_count = recomment_list_pagination.num_pages
                nexts = None
                previous = None
                if int(page) > recomment_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if recomment_count != 1:
                        nexts = f'/api/recomments/?post={comment_id}&page=2'
                else:
                    if page == str(recomment_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/comments/?post={comment_id}&page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/comments/?post={comment_id}&page={page_str_next}'
                        previous = f'/api/comments/?post={comment_id}&page={page_str_pre}'
                return JsonResponse({'results':{'id':int(comment_id),'page':recomment_page,'count':recomment_count},'next':nexts,'previous':previous}, safe=False)
        return JsonResponse({'results':{'id':int(comment_id),'page':recomment_page,'count':recomment_count},'next':nexts,'previous':previous}, safe=False)



# 코멘트 뷰셋

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def list(self,request):
        queryset = Comment.objects.all().order_by('-created_at')
        serializer_class = CommentSerializer
        post_id = request.GET.get('post')
        if post_id:
            queryset = Post.objects.all()
            postparents = get_object_or_404(queryset, pk=post_id)
            commentpost = list(postparents.comments.values().order_by('-created_at'))
            page = request.GET.get('page')
            if page:
               # 여기 페이지 수 조절할것
                comment_list_pagination = Paginator(commentpost,5)
                comment_page = list(comment_list_pagination.get_page(page))
                # 프로필 이미지 넣기
                recomment_set = [{}]
                if len(comment_page) != 0:
                    comment_temp = []
                    recomment_set = [{}]
                    for comment_item in comment_page:
                        comment_id = comment_item['commenter']
                        profile_query = Profile.objects.all()
                        commenter = get_object_or_404(profile_query, pk=comment_id)
                        # commenter_value = list(commenter)
                        comment_item['user_image'] = commenter.user_image
                        comment_item['nickname'] = commenter.nickname
                        comment_item['permission'] = commenter.permission


                        # 리코멘트 페이지 1
                        commentparentid = comment_item['id']
                        commentqueryset = Comment.objects.get(id=commentparentid)
                        recommentchild = list(commentqueryset.recomments.values().order_by('-created_at'))
                        # recomment_temp = [{'count':0,'id':commentparentid,'page':[]}]
                        recomment_setitem = {'id':commentparentid,'count':0,'page':[]}
                        if len(recommentchild) != 0:
                            recomment_list_pagination = Paginator(recommentchild,5)
                            recomment_page = list(recomment_list_pagination.get_page(1))
                            recomment_child_count = recomment_list_pagination.num_pages


                            for recomment_item in recomment_page:
                                recomment_id = recomment_item['commenter']
                                profile_query = Profile.objects.all()
                                recommenter = get_object_or_404(profile_query, pk=recomment_id)
                                # commenter_value = list(commenter)
                                recomment_item['user_image'] = recommenter.user_image
                                recomment_item['nickname'] = recommenter.nickname
                                recomment_item['permission'] = recommenter.permission

                            recomment_setitem = {'id':commentparentid,'count':recomment_child_count,'page':recomment_page}
                            # recomment_temp = [{'count':recomment_child_count,'id':commentparentid,'page':recomment_page}]
                        recomment_set.append(recomment_setitem)
                        # comment_item['recomments'] = recomment_temp



                # 프로필 뽑기 전처리
                comment_count = comment_list_pagination.num_pages
                nexts = None
                previous = None
                if int(page) > comment_count or int(page) <= 0:
                    return Response('error')
                if int(page) == 1:
                    if comment_count != 1:
                        nexts = f'/api/comments/?post={post_id}&page=2'
                else:
                    if page == str(comment_count):
                        page_str = str(int(page)-1)
                        previous = f'/api/comments/?post={post_id}&page={page_str}'
                    else:
                        page_str_next = str(int(page)+1)
                        page_str_pre =  str(int(page)-1)
                        nexts = f'/api/comments/?post={post_id}&page={page_str_next}'
                        previous = f'/api/comments/?post={post_id}&page={page_str_pre}'
                return JsonResponse({'results':comment_page,'count':comment_count,'next':nexts,'previous':previous,'recomment':recomment_set}, safe=False)
        return JsonResponse({'results':[],'count':comment_count,'next':nexts,'previous':previous,'recomment':recomment_set}, safe=False)


