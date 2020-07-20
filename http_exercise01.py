"""
http
浏览器多次访问
"""

from socket import *

# 创建tc套接字
s = socket()
s.bind(('0.0.0.0', 8800))
s.listen(5)

while True:
    c, addr = s.accept()
    print('Connect from', addr)  # 浏览器连接
    data = c.recv(4096)  # 接收的是http请求
    print(data.decode().split('\r\n')[0])  # 只看请求行  即第一行

    # http响应格式（严格的格式，差一点都行）
    f = open('index.html')
    info = f.read()
    html = 'HTTP/1.1 200 OK\r\n'
    html += "Content-Type:text/html\r\n"
    html += '\r\n'
    html += f.read() # 响应体
    f.close()
    # html = """HTTP/1.1 200 OK
    # Content-Type:text/html
    #
    # %s
    # """

    c.send(html.encode())  # 发送响应给客户端
    c.close()
    s.close()

# 每一次请求都是从重新的连接开始的