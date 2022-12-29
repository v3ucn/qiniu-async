## 安装

通过pip

```bash
$ pip install qiniu-async
```

## 使用方法

### 上传
```python
import asyncio
import qiniu_async


q = qiniu_async.Qiniu(access_key,access_secret)

token = q.upload_token(bucketname)

# 文件流上传
asyncio.run(q.upload_data(token,"333.txt","123测试"))

# 文件地址上传
asyncio.run(q.upload_file(token,"mypic0.jpeg","/Users/liuyue/Downloads/mypic0.jpeg"))


### 异步框架接入

#### Tornado

```python
import qiniu_async

async def post(self):

    file = self.request.files['file']

    for meta in file:
        filename = meta['filename']

        q = qiniu_async.Qiniu(access_key,access_secret)

        token = q.upload_token(bucketname)

        await q.upload_data(token,filename,meta['body'])
        

    return self.write('Your file has been uploaded')

```
