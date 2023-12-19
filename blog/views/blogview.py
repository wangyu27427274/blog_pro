from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models
from blog.ext.hook import MyHook
from blog.ext.auth import URLAuth
from datetime import datetime
"""博客序列化类"""


class Blogserializer(MyHook, serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = ['id','category','image','title','summary','text','creator','comment_count','favor_count']
        extra_kwargs = {
            'creator':{'read_only':True},
            'comment_count': {'read_only': True},
            'favor_count': {'read_only': True},
            'text': {'write_only': True},

        }

    def Myhook_creator(self, obj):
        return obj.creator.username

    def Myhook_category(self, obj):
        return obj.get_category_display()


"""评论序列化类"""


class Comserializer(MyHook, serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"

    def Myhook_user(self, obj):
        return obj.user.username

    def Myhook_blog(self, obj):
        return obj.blog.title

    def  Myhook_create_datetime(self, obj):
        return obj.create_datetime.strftime("%Y-%m-%d:%H:%M:%S")

"""展示博客列表与创建博客"""


class BlogView(APIView):
    # 登陆验证
    authentication_classes = [URLAuth, ]
    """展示博客列表"""

    def get(self, request, *args, **kwargs):
        query_set = models.Blog.objects.all().order_by('-id')
        res = Blogserializer(instance=query_set, many=True)
        content = {
            'status': 10086,
            'data': res.data
        }

        return Response(content)

    """新建博客"""

    def post(self, request):
        if not request.user:
            return Response({'status': 10087, 'msg': '请先登录'})
        ser =  Blogserializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': 10087, 'msg': '数据格式错误','detail': ser.errors})
        ser.save(ctime=datetime.now(), creator=request.user)
        return Response({'status': 10086, 'msg': '创建成功', 'data': ser.data})

"""查看博客详情与评论"""


class BlogViewdetail(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        """获取博客内容"""
        queryblog_obj = models.Blog.objects.filter(id=pk).first()

        if not queryblog_obj:
            return Response({'status': 10087, 'msg': '数据不存在'})
        """获取博客相关评论"""
        querycom_set = models.Comment.objects.filter(blog=queryblog_obj).all()

        res_blog = Blogserializer(instance=queryblog_obj, many=False)
        res_com = Comserializer(instance=querycom_set, many=True)
        content = {
            'status': 10086,
            'data': res_blog.data,
            'comment': res_com.data
        }

        return Response(content)
