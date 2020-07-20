"""
基于poll方法实现IO并发

"""

from socket import *
from select import *
from time import sleep

#  全局变量

HOST = '0.0.0.0'
PORT = 8889
ADDR = (HOST, PORT)

# 创建套接字   是监听套接字
tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(5)

# 设置为非阻塞
tcp_socket.setblocking(False)

p = poll()  # 建立poll对象
p.register(tcp_socket, POLLIN)  # 初始监听对象,POLLIN是关注的事件，读事件

#  准备工作，建立文件描述符和IO对象对应的字典  时刻与register的IO一致
map = {tcp_socket.fileno(): tcp_socket}  # 以文件描述符为键，以对象为值

# 循环监听
while True:
    #  对关注的IO进行监控
    events = p.poll()  # 监控的返回值 events
    # events--->[(fileno,event),().....]  每个元组代表一个就绪的IO
    # 第一项是就绪IO的文件秒数符，第二项是事件
    for fd, event in events:  # 用两个变量去取这个值
        #  分情况讨论
        if fd == tcp_socket.fileno():  # 监听套接字的处理
            #  处理客户端连接
            connfd, addr = map[fd].accept()  # 接收来自客户端的连接，用IO对象
            print('Connect from', addr)
            connfd.setblocking(False)  # 设置非阻塞
            p.register(connfd, POLLIN)  # 添加到监控
            map[connfd.fileno()] = connfd  # 同时维护字典

        elif event == POLLIN:  # 客户端的连接套接字的处理
            # 收消息
            data = map[fd].recv(1024)
            if not data:
                # 客户端退出
                p.unregister(fd)  # 移除关注
                map[fd].close()
                del map[fd]  # 从字典也移除
                continue  # 这里使用continue，是因为这是在for循环里，如果有一个客户端退出了，此时break，其他的就都无法执行了，第一个退出了，继续取后面的
            print(data.decode())
            p.register(fd,POLLOUT)#参数是文件对象，还是文件描述符都可以.关注写
        elif event & POLLOUT:
            map[fd].send(b'OK')
            p.register(fd,POLLIN)

