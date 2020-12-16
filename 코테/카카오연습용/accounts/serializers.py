from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from .models import Post, Profile
from .models import Comment, Recomment
from .models import Notice,Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# 등록


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        return user

# 로그인


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "인증 불가")

# 확인


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','is_staff')

# 리코멘터링


class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = '__all__'

# 코멘트


class CommentSerializer(serializers.ModelSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

# 포스트 

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at',)


# 포스트 라이크

class PostLikeSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at',)


# 포스트 찾기

class PostSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'username','created_at',)
        read_only_fields = ('created_at',)

# 프로필 찾기
class ProfileSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'user_image','username',)


# 미니 리스트(검색용)


class MiniListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'username','created_at',)



# 갤러리


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


# 메인 리스트(검색용)


class MainListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'username','created_at',)
        

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileEmailSerializer(serializers.ModelSerializer):
    myposts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class MiniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ListProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'user_image','username','facebook','instargram','twitter','kakaotalk','permission',)

# 무한스크롤 & 페이지네이션


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 1000

# 공지
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


# 이벤트

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

# 이벤트 조인

class EventJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =  ('user', )
    
