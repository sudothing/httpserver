#coding=utf-8
'''
name : xin
time : 2019.8.15
'''

from socket import *
import sys,re,signal
from threading import Thread
import time,traceback
from settings import *


class HTTPServer(object):
    def __init__(self,addr=('0.0.0.0',80)):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind(addr)

    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    def server_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d...'%self.port)
        while True:
            try:
                confd,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                sys.exit('服务器退出')
            except Exception:
                traceback.print_exc()
                continue
            print('Connect from',addr)
            handle_client = Thread(target=self.handle_request,args=(confd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self,confd):
        #接受浏览器请求
        request = confd.recv(4096)
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode()
        #正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headlers = 'HTTP/1.1 500 Server Error\r\n'
            response_headlers += '\r\n'
            response_body = 'Server Error'
            response = response_headlers +response_body
            confd.send(response.encode())
            return

        #将请求发给WebFrame得到返回的数据结果
        status,response_body = \
            self.send_request(env['METHOD'],env['PATH'])
        #根据响应码组织响应头内容
        response_headlers = self.get_headlers(status)
        #将结果组织为http response发送给客户端
        response = response_headlers + response_body
        confd.send(response.encode())
        confd.close()

    #和WebFrame交互，发送request获取response
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)
        #向WebFrame发送method和path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())
        #等待接收WebFrame回发的结果
        status = s.recv(128).decode()
        response_body = ''
        while True:
            body = s.recv(4096).decode()
            if body == '###':
                break
            response_body += body
        return status,response_body

    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 ok\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'
        return response_headlers


if __name__ == '__main__':
    ADDR
    httpd = HTTPServer(ADDR)
    httpd.server_forever()
