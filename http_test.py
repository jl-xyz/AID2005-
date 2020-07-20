"""
http请求响应演示
"""
from socket import *

# 创建tc套接字
s = socket()
s.bind(('0.0.0.0', 8800))
s.listen(5)

c, addr = s.accept()
print('Connect from',addr)  #浏览器连接
data = c.recv(4096)   #接收的是http请求
print(data.decode())

# http响应格式（严格的格式，差一点都行）
html = """HTTP/1.1 200 OK    
Content-Type:text/html       
                            
hello world                 
"""

# http响应格式（严格的格式，差一点都行）
# html = """HTTP/1.1 200 OK    #响应行
# Content-Type:text/html       #响应头
#                              #空行
# hello world                  #响应体
# """

# html = """HTTP/1.1 404 Not Found
# Content-Type:text/html
#
# Sorry.....
# """


c.send(html.encode()) # 发送响应给客户端


c.close()
s.close()
