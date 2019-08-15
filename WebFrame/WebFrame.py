#coding=utf-8
'''
name : xin
time : 2019.8.15
'''

import sys
import time
from socket import *

from settings import *
from urls import *
from views import *

class Application(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(frame_addr)

    def start(self):
        self.sockfd.listen(5)
        while True:
            confd,addr = self.sockfd.accept()
            #接收请求方法
            method = confd.recv(128).decode()
            #接收请求内容
            path =confd.recv(128).decode()
            print(method,path)
            if method == 'GET':
                if path == '/' or path[-5:] == '.html':
                    status , response_body = self.get_html(path)
                else:
                    status , response_body = self.get_data(path)
                #将结果发送到httpserver
                confd.send(status.encode())
                time.sleep(0.1)
                confd.send(response_body.encode())
                time.sleep(0.1)
                confd.send(b'###')

            elif method == 'POST':
                pass

    def get_html(self,path):
        if path == '/':
            get_file = static_dir + '/index.html'
        else:
            get_file = static_dir + path
        try:
            f = open(get_file)
        except IOError:
            response = ('404','===Sorry not found the page===')
        else:
            response = ('200',f.read())
        finally:
            return response

    def get_data(self,path):
        for url,handler in urls:
            if path == url:
                response_body = handler()
                return '200',response_body
        return '404','Sorry,Not found the data'




if __name__ == '__main__':
    app = Application()
    app.start()#启动框架等待request
