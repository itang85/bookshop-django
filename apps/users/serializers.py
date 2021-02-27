from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from apps.users.models import *


# 登录
class postLoginViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class postSignupViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    nick_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()


class getUserViewSerializer(serializers.Serializer):
    _data = serializers.JSONField(required=False)

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['_data'] = {
            'id': now_user.id,
            'username': now_user.username,
            'mobile': now_user.mobile[:3] + '****' + now_user.mobile[-4:],
            'email': now_user.email,
            'id_num': now_user.id_num[:4] + '**********' + now_user.id_num[-4:],
            'nick_name': now_user.nick_name,
            'signature': now_user.signature,
            'region': now_user.region,
            'avatar_url': now_user.avatar_url,
            'gender': now_user.gender,
            'gender_cn': now_user.get_gender_display(),
            'birth_date': now_user.birth_date,
            'last_login': now_user.last_login,
            'roles': now_user.auth.get_routers,
            'group': now_user.group.group_type
        }
        return attrs


class postUserViewSerializer(serializers.Serializer):
    pass


class putUserViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    real_name = serializers.CharField(required=False)
    id_num = serializers.CharField(required=False)
    nick_name = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    avatar_url = serializers.URLField(required=False)
    gender = serializers.CharField(required=False)
    birth_date = serializers.CharField(required=False)
    signature = serializers.CharField(required=False)


class getShippingAddressViewSerializer(serializers.Serializer):
    def validate(self, attrs):
        now_user = self.context['request'].user
        obj_address = ShippingAddressModel.objects.filter(receiver_id=now_user.id).values()
        attrs = list(obj_address)
        return attrs

class postShippingAddressViewSerializer(serializers.Serializer):
    real_name = serializers.CharField()
    mobile = serializers.CharField()
    region = serializers.CharField()
    address = serializers.CharField()

    def validate(self, attrs):
        now_user = self.context['request'].user
        attrs['receiver'] = UserModel.objects.filter(id=now_user.id).first()
        return attrs

class putShippingAddressViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    real_name = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

class deleteShippingAddressViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()



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
