from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.TextField(blank=True)
    nickname = models.TextField(blank=True)
    email = models.TextField(blank=True)
    description = models.TextField(blank=True)
    user_image = models.TextField(blank=True)
    nationality = models.TextField(blank=True)
    skill = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    level = models.TextField(blank=True)
    ispublic = models.BooleanField(blank=True, default=True)

    facebook = models.TextField(blank=True)
    instargram = models.TextField(blank=True)
    twitter = models.TextField(blank=True)
    kakaotalk = models.TextField(blank=True)
    permission = models.IntegerField(blank=True, default=4)
    # 포스트
    posts = models.ManyToManyField(
        'Post', blank=True, related_name='like_users')
    # 팔로워 팔로잉
    follower = models.ManyToManyField(
        "self", symmetrical=False, related_name='followers', blank=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name='followings', blank=True)
    # 참여 이벤트
    event = models.ManyToManyField('Event',blank=True,related_name='join_event')

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.TextField(blank=True)
    start = models.DateTimeField(blank=True)
    organizer = models.IntegerField(blank=True)
    content = models.TextField(blank=True)
    background = models.TextField(blank=True)
    place_name = models.TextField(blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    profile = models.ManyToManyField('Profile',blank=True,related_name='join_people')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

class Notice(models.Model):
    title = models.CharField(max_length=144, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    image_url = models.TextField(blank=True)
    image_file = models.FileField(upload_to="%Y/%m/%d", blank=True)
    viewcount = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Post(models.Model):
    profileid = models.ForeignKey(
        'Profile', related_name='myposts', on_delete=models.CASCADE, blank=True)
    # foreignkey
    username = models.TextField(blank=True)
    title = models.CharField(max_length=144, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    viewcount = models.IntegerField(default=0)
    profiles = models.ManyToManyField(
        'Profile', blank=True, related_name='like_posts')
    numlike = models.IntegerField(default=0)
    numcomment = models.IntegerField(default=0)
    category = models.TextField(default='board')
    # image_file = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True)
    # image_url = models.TextField(blank=True)
    YouTube = models.TextField(default="",blank=True)
    image_file = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True, height_field="height",
        width_field="width",)
    image_url = models.TextField(blank=True)
    width = models.IntegerField(blank=True, null=True,default=1)
    height = models.IntegerField(blank=True, null=True,default=1)
    def __str__(self):
        return self.title



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, 
        user_id=instance.id,
        username=instance.username,
        email=instance.email,
        nickname=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# 코멘트
class Comment(models.Model):
    postid = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE, blank=True)
    commenter = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.TextField()
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 리코멘트
class Recomment(models.Model):
    commentid = models.ForeignKey(
        'Comment', related_name='recomments', on_delete=models.CASCADE, blank=True)
    commenter = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.TextField()
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.name