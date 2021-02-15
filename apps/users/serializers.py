from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from apps.users.models import *


class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# 新增后台用户使用
class AddUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        exclude = ('deleted',)
        validators = [
            UniqueTogetherValidator(queryset=UserModel.objects.all(), fields=['mobile',], message='该手机号已经存在'),
            UniqueTogetherValidator(queryset=UserModel.objects.all(), fields=['email',], message='该邮箱已经存在'),
            UniqueTogetherValidator(queryset=UserModel.objects.all(), fields=['username',], message='该登录名已经存在')
            ]

    def validate(self, attrs):
        now_user = self.context['request'].user
        print(attrs['group'].group_type)
        if attrs['group'].group_type == 'SuperAdmin' and now_user.group.group_type != 'SuperAdmin':
            raise serializers.ValidationError("无权建立超级管理员账号。")
        # if attrs['group'].group_type == 'NormalUser' and now_user.group.group_type != 'SuperAdmin':
        #     raise serializers.ValidationError("无权私自建立普通用户账号。")
        return attrs


# 新增权限菜单约束使用
class AddAuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermissionModel
        fields = ['id', 'object_name', 'object_name_cn', 'auth_list', 'auth_create', 'auth_update', 'auth_destroy']


# 返回权限使用
class ReturnAuthSerializer(serializers.ModelSerializer):
    auth_permissions = AddAuthPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = AuthModel
        exclude = ('deleted',)


# ReturnUserSerializer 使用的group序列化器
class UserUseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        exclude = ('deleted',)

    # 返回用户使用 userinfo也使用


class ReturnUserSerializer(serializers.ModelSerializer):
    group = UserUseGroupSerializer()
    auth = ReturnAuthSerializer()

    class Meta:
        model = UserModel
        exclude = ('deleted', 'password',)


# 修改后台用户使用
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('deleted',)
        validators = [
            UniqueTogetherValidator(queryset=UserModel.objects.all(), fields=['mobile', ], message='该手机号已经存在'),
            UniqueTogetherValidator(queryset=UserModel.objects.all(), fields=['username', ], message='该登录名已经存在')
        ]

    def validate(self, attrs):
        now_user = self.context['request'].user
        if attrs.get('group') and now_user.group.group_type != 'SuperAdmin':
            raise serializers.ValidationError("无权修改用户组。")
        return attrs
