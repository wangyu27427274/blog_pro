from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models
from blog.ext.hook import MyHook
class Blogserializer(MyHook,serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = "__all__"

    def Myhook_creator(self,obj):
        return obj.creator.username


class BlogView(APIView):
    def get(self, request,*args,**kwargs):
        query_set = models.Blog.objects.all().order_by('-id')
        res = Blogserializer(instance=query_set, many=True)
        content = {
            'status': 10086,
            'data': res.data
        }

        return Response(content)

