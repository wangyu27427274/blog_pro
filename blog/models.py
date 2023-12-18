from django.db import models



"""
用户信息
"""
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名' ,max_length=32,db_index=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    token =  models.CharField(verbose_name='token',max_length=64,null=True,blank=True,db_index=True)

"""
博客信息
"""
class Blog(models.Model):
    category_list = ((1,"云计算"),(2,"Python全栈"),(3,"Go开发"))
    category = models.SmallIntegerField(verbose_name='分类',choices=category_list)

    image = models.CharField(verbose_name='封面',max_length=255)
    title = models.CharField(verbose_name='标题',max_length=32)
    summary = models.CharField(verbose_name='简介',max_length=255)
    text =  models.TextField(verbose_name='博文')
    ctime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    creator = models.ForeignKey(verbose_name='创建者',to='UserInfo',on_delete=models.CASCADE)
    comment_count = models.PositiveIntegerField(verbose_name='评论数',default=0)
    favor_count = models.PositiveIntegerField(verbose_name='点赞数',default=0)

"""
点赞信息
"""
class Favor(models.Model):
    blog = models.ForeignKey(verbose_name='博客',to='Blog',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='用户',to='UserInfo',on_delete=models.CASCADE)
    creat_datetime =  models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    #创建联合索引
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog','user'],name='unique_favor_blog_user')
        ]

"""
评论表
"""
class Comment(models.Model):
    blog = models.ForeignKey(verbose_name='博客',to='Blog',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='用户',to='UserInfo',on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容',max_length=150)
    create_datetime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)






