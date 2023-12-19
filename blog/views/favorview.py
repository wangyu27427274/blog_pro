from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models
from blog.ext.auth import URLAuth, NoAuth
from datetime import datetime
from django.db.models import F
"""点赞序列化类"""


class Favorserializers(serializers.ModelSerializer):
    class Meta:
        model = models.Favor
        fields = ["id", "user", "blog"]
        extra_kwargs = {
            "user": {"read_only": True},
            "blog": {"read_only": True},
        }


"""点赞"""


class FavorView(APIView):
    # 必须进行登录验证且必须登录
    authentication_classes = [URLAuth, NoAuth, ]

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        ser = Favorserializers(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)

        exists = models.Favor.objects.filter(blog_id=blog_id, user=request.user).exists()
        if exists:
            return Response({"msg": "你已经点赞过啦"})

        ser.save(blog_id=blog_id, user=request.user,creat_datetime=datetime.now())
        #点赞成功后,博客点赞统计数加1
        models.Blog.objects.filter(id=blog_id).update(favor_count=F('favor_count') + 1)
        return Response({"msg": "点赞成功","data": ser.data})