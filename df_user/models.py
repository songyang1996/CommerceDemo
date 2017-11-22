from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from celery import Celery
import re
# Create your models here.

class PassportManager(models.Manager):
    '''账户模型管理器类'''
    def save_account(self, username, password, email):
        '''保存一个用户信息'''
        # 密码使用sha1算法加密
        passport = self.create(username=username, password=get_hash(password), email=email)
        return passport

    def get_account(self, username, password=None):
        '''根据用户名查询用户信息'''
        # 此函数目前封装用于登录的重复验证
        try:
            if password:
                passport = self.get(username=username, password=get_hash(password))
            else:
                passport = self.get(username=username)
        except self.model.DoesNotExist:
            passport = None
        return passport


class Passport(BaseModel):
    '''账户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    is_activate = models.BooleanField(default=False, verbose_name='激活状态')
    objects = PassportManager()

    def generate_active_token(self):
        '''导入itsdangerous模块 生成激活用的token信息'''
        serializer = Serializer(settings.SECRET_KEY, 3600)  # 使用setting里的secretkey作为加密key 这段字符串是哎startproject时生成的  过期时间为3600s
        token = serializer.dumps({'confirm': self.id})
        return token.decode()  # 加密后为byte格式 需要转为unicode格式

    class Meta:
        db_table = 's_user_account'

class PassportInfoManager(models.Manager):

    def get_address(self, passport_id):
        '''查询默认的收货地址'''
        try:
            address = self.get(passport_id=passport_id, is_default=True)
        except self.model.DoesNotExist:
            address = None
        return address

    def save_address(self, passport_id, name, addr, zip_code, phone):
        '''添加一个新的收货地址'''
        address = self.get_address(passport_id)
        # 判断有没有默认收货地址 如果不能支持多选 这个逻辑没什么用
        if address:
            # 有默认收货地址
            is_default = False
        else:
            # 没有默认收货地址
            is_default = True

        address = self.create(passport_id=passport_id, name=name, addr=addr, zip_code=zip_code, phone=phone, is_default=is_default)

        return address

class PassportInfo(BaseModel):
    '''账户详情模型类'''
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    name = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=40, verbose_name='详细地址')
    zip_code = models.CharField(max_length=10, verbose_name='邮政编码')
    phone = models.CharField(max_length=20, verbose_name='手机')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    objects = PassportInfoManager()

    class Meta:
        db_table = 's_user_address'
