from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models
from blog.ext.hook import MyHook
from blog.ext.auth import URLAuth
from datetime import datetime
from django.db.models import F
"""评论序列化类"""


class CommentSerializer(MyHook, serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True},
            'id': {'read_only': True},
            'blog': {'read_only': True},
            'create_datetime': {'read_only': True},
        }

    def Myhook_user(self, obj):
        return obj.user.username

    def Myhook_blog(self, obj):
        return obj.blog.title

    def  Myhook_create_datetime(self, obj):
        return obj.create_datetime.strftime("%Y-%m-%d:%H:%M:%S")

"""评论列表"""


class CommentView(APIView):
    #对登录用户进行验证
    authentication_classes = [URLAuth,]

    """获取评论列表(无需验证)"""
    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        querycom_obj = models.Comment.objects.filter(blog_id=blog_id)
        if not querycom_obj:
            return Response({"msg": "数据不存在"})
        ser = CommentSerializer(querycom_obj, many=True)
        return Response(ser.data)

    """添加评论(需要验证)"""
    def post(self,request, *args, **kwargs):
        if not request.user:
            return Response({"msg": "请先登录"})

        blog_id = kwargs.get("blog_id")
        blog_object = models.Blog.objects.filter(id=blog_id).first()
        if not blog_object:
            return Response({"msg": "博客不存在"})

        ser = CommentSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": 10087, "error": "校验失败", "detail": ser.errors})

        ser.save(blog=blog_object, user=request.user,create_datetime=datetime.now())
        # 点赞成功后,博客点赞统计数加1
        models.Blog.objects.filter(id=blog_id).update(comment_count=F('comment_count') + 1)
        return Response({"status": 10086, "sucess": "评论成功", "detail": ser.data})





