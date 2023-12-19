from rest_framework.authentication import BaseAuthentication
from blog import models
from rest_framework import exceptions

class URLAuth(BaseAuthentication):
    def authenticate(self, request):

        token = request.query_params.get('token')
        #如果请求中没有token信息,则进行匿名访问问
        if not token:
            return

        instance = models.UserInfo.objects.filter(token=token).first()
        #如果请求信息当中的token查询不到数据,则进行匿名访问问
        if not instance:
            return
        return instance, token

    def authenticate_header(self, request):

        return "API"


class NoAuth(BaseAuthentication):
    def authenticate(self, request):

        raise exceptions.AuthenticationFailed({"status":10087,"message":"请登录"})

    def authenticate_header(self, request):

        return "API"