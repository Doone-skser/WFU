import time
import requests
import sys


def progressbar(url, name):
    path = sys.path[0]
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['Content-Length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            filepath = path + '\\' + name  # 设置图片name，注：必须加上扩展名
            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    now_data = float(size / content_size * 100)
                    print('\r' + '[下载进度]:%.2f%%' % now_data, end='')
                    # print('\r' + '[下载进度]:%.2f%%' % (float(size / content_size * 100)), end='')
            end = time.time()  # 下载结束时间
            costTime = end - start
            print()
            print('%0.2f' % costTime)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    progressbar(url='https://oss.nvidia.fun/%E6%A0%A1%E5%9B%AD%E7%BD%91%E5%8A%A9%E6%89%8B.exe', name='abc.exe')