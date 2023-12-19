"""
URL configuration for blog_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import blogview, account, commmentview,favorview

urlpatterns = [
    ###博客列表与详情###
    path('api/blog/', blogview.BlogView.as_view(), name='blog'),
    path('api/blog/<int:pk>', blogview.BlogViewdetail.as_view(), name='blogdetail'),
    ###登陆与注册路由###
    path('api/register/', account.RegisterView.as_view(), name='register'),
    path('api/login/', account.LoginView.as_view(), name='login'),
    ###评论列表与添加###
    path('api/comment/<int:blog_id>', commmentview.CommentView.as_view(), name='comment'),
    ###点赞###
    path('api/favor/<int:blog_id>', favorview.FavorView.as_view(), name='favor'),
]
