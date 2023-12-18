import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from blog import models

"""用户注册序列化类"""


class Registerserializers(serializers.ModelSerializer):
    # 密码验证
    confirm_password = serializers.CharField(max_length=64, min_length=6, required=True, write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password']
        """:param
        id : 字段只展示，不校验
        password : 字段只校验，不展示        
        """
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def validate_confirm_password(self, value):
        # 获取注册信息
        password = self.initial_data['password']
        if password != value:
            raise serializers.ValidationError("两次密码不一致")
        return value


"""用户注册"""


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):

        ser = Registerserializers(data=request.data)
        if ser.is_valid():
            # 删除验证密码字段
            ser.validated_data.pop('confirm_password')
            ser.save()
            return Response({"status": 10086, "sucess": "注册成功", "detail": ser.data})
        else:
            return Response({"status": 10087, "error": "注册失败", "detail": ser.errors})


"""用户登录序列化类"""


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

"""用户登录"""


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"status": 10087, "error": "校验失败", "detail": ser.errors})
        # ser.validated_data为请求对象数据字典
        instance = models.UserInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"status": 10088, "error": "用户名或密码错误"})
        #生成token并且进行保存
        token = str(uuid.uuid4())
        instance.token = token
        instance.save()
        return Response({"status": 10086, "sucess": "登录成功", "detail":  {"token": token}})
