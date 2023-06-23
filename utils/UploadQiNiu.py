#引入相关类及函数
from qiniu import Auth,put_data,put_file

#上传文件类
class UploadQiNiu:

    #只支持单文件上传
    def __init__(self,config):
        self.access_key = config['access_key']
        self.secret_key = config['secret_key']
        self.bucket_name = config['bucket_name']
        self.domain = config['domain']
        #初始化对接
        self._q = Auth(self.access_key, self.secret_key)

    # 上传本地文件
    # source_file_path 本地文件路径
    # save_file_name 上传到七牛云上保存时的名字
    def uploadFile(self, source_file_path, save_file_name):
        #生成上传token
        token = self._q.upload_token(self.bucket_name, save_file_name)
        #上传文件
        ret, info = put_file(token, save_file_name, source_file_path)
        #根据返回信息判断是否上传成功
        if info.status_code == 200:
            #返回链接
            return '/' . join([self.domain, save_file_name])
        return None

    #上传二进制文件流
    # file_data 文件流数据（二进制数据）
    # save_file_name 上传到七牛云上保存时的名字
    def uploadData(self,file_data, save_file_name):
        #生成上传token
        token = self._q.upload_token(self.bucket_name, save_file_name)
        #上传文件
        ret, info = put_data(token, save_file_name, file_data)
        if info.status_code == 200:
            return '/' . join([self.domain, save_file_name])
        return None

#相关配置（我的配置不会怎么变，所以放在这里全局引用，根据自己情况来）
config = {
    'access_key': '',  # 填你的access_key
    'secret_key': '',  # 填你的secret_key
    'bucket_name': '',  # 填你的存储空间名称
    'domain': ''  # 填你的空间域名
}

#外部调用直接引入以下两个函数就行了
#上传本地文件
def uploadFile(source_file_path:str,save_file_name:str):
    try:
        uploadQiNiu = UploadQiNiu(config)
        url = uploadQiNiu.uploadFile(source_file_path,save_file_name)
        return url
    except:
        return False

#上传二进制文件
def uploadData(data:str,save_file_name:str):
    try:
        uploadQiNiu = UploadQiNiu(config)
        url = uploadQiNiu.uploadData(data,save_file_name)
        return url
    except:
        return False

#测试
if __name__ == '__main__':
    #上传同目录下的ceshi.md文件
    with open( 'ceshi.md', 'rb') as f:
        #以文件流形式上传
        url = uploadData(f.read(), 'ceshi.md')
        print(url)
