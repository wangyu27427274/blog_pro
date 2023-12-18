from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models
from blog.ext.hook import MyHook

"""博客序列化类"""
class Blogserializer(MyHook, serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = "__all__"

    def Myhook_creator(self, obj):
        return obj.creator.username


    def Myhook_category(self, obj):
        return obj.get_category_display()

"""评论序列化类"""
class Comserializer(MyHook, serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


    def  Myhook_user(self,obj):
        return obj.user.username


    def Myhook_blog(self,obj):
        return obj.blog.title

"""展示博客列表"""
class BlogView(APIView):
    def get(self, request, *args, **kwargs):
        query_set = models.Blog.objects.all().order_by('-id')
        res = Blogserializer(instance=query_set, many=True)
        content = {
            'status': 10086,
            'data': res.data
        }

        return Response(content)


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

