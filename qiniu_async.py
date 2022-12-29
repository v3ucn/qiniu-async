# @Author:Liu Yue (v3u.cn)
# @Software:Vscode
# @Time:2022/12/30

import base64
import hmac
import time
from hashlib import sha1
import json
import httpx
import aiofiles



class Qiniu:

    def __init__(self, access_key, secret_key):
        """初始化"""
        self.__checkKey(access_key, secret_key)
        self.__access_key = access_key
        self.__secret_key = secret_key.encode('utf-8')

    def get_access_key(self):
        return self.__access_key

    def get_secret_key(self):
        return self.__secret_key

    def __token(self, data):
        hashed = hmac.new(self.__secret_key,data.encode('utf-8'), sha1)
        return self.urlsafe_base64_encode(hashed.digest())

    def token(self, data):
        return '{0}:{1}'.format(self.__access_key, self.__token(data))

    def token_with_data(self, data):
        data = self.urlsafe_base64_encode(data)
        return '{0}:{1}:{2}'.format(
            self.__access_key, self.__token(data), data)

    def urlsafe_base64_encode(self,data):

        if isinstance(data, str):
            data = data.encode('utf-8')

        ret = base64.urlsafe_b64encode(data)

        data = ret.decode('utf-8')

        return data


    @staticmethod
    def __checkKey(access_key, secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')


    def upload_token(
            self,
            bucket,
            key=None,
            expires=3600,
            policy=None,
            strict_policy=True):
        """生成上传凭证

        Args:
            bucket:  上传的空间名
            key:     上传的文件名，默认为空
            expires: 上传凭证的过期时间，默认为3600s
            policy:  上传策略，默认为空

        Returns:
            上传凭证
        """
        if bucket is None or bucket == '':
            raise ValueError('invalid bucket name')

        scope = bucket
        if key is not None:
            scope = '{0}:{1}'.format(bucket, key)

        args = dict(
            scope=scope,
            deadline=int(time.time()) + expires,
        )

        return self.__upload_token(args)

    @staticmethod
    def up_token_decode(up_token):
        up_token_list = up_token.split(':')
        ak = up_token_list[0]
        sign = base64.urlsafe_b64decode(up_token_list[1])
        decode_policy = base64.urlsafe_b64decode(up_token_list[2])
        decode_policy = decode_policy.decode('utf-8')
        dict_policy = json.loads(decode_policy)
        return ak, sign, dict_policy

    def __upload_token(self, policy):
        data = json.dumps(policy, separators=(',', ':'))
        return self.token_with_data(data)


    @staticmethod
    def __copy_policy(policy, to, strict_policy):
        for k, v in policy.items():
            if (not strict_policy) or k in _policy_fields:
                to[k] = v

    # 上传文件流
    async def upload_data(self,up_token, key,data,url="http://up-z1.qiniup.com",params=None,mime_type='application/octet-stream',file_name=None,metadata=None):

        data.encode('utf-8')
        
        fields = {}
        if params:
            for k, v in params.items():
                fields[k] = str(v)

        if key is not None:
            fields['key'] = key
        fields['token'] = up_token

        fname = file_name
        if not fname or not fname.strip():
            fname = 'file_name'

        async with httpx.AsyncClient() as client:

            # 调用异步使用await关键字
            res = await client.post(url,data=fields,files={'file': (fname,data,mime_type)})

            print(res.text)

    # 上传文件实体
    async def upload_file(self,up_token,key,path,url="http://up-z1.qiniup.com",params=None,mime_type='application/octet-stream',file_name=None,metadata=None):


        async with aiofiles.open(path, mode='rb') as f:
            contents = await f.read()
        
        fields = {}
        if params:
            for k, v in params.items():
                fields[k] = str(v)

        if key is not None:
            fields['key'] = key
        fields['token'] = up_token

        fname = file_name
        if not fname or not fname.strip():
            fname = 'file_name'

        async with httpx.AsyncClient() as client:

            # 调用异步使用await关键字
            res = await client.post(url,data=fields,files={'file': (fname,contents,mime_type)})

            print(res.text)





