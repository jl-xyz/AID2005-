"""
web服务程序
假定：用户有一组网页，希望使用我们提供的类快速搭建一个服务，
实现自己网页的展示浏览

主要功能：
1，接收客户端（浏览器）发请求
2，


对功能进行类封装设计
1.  从功能的使用方法的角度分析
    就是先不要想类里面具体怎么实现，
    如果你是使用者，拿到类，想怎么用

    (创建进程，创建线程，套接字)

2.  借鉴自己曾经用过的python类

    socket()  套接字类怎么用的
    首先实例化对象-----》用户可以选择何种套接字（不同的套接字功能不同）
    通过传入不同的参数，可以选择创建不同的对象
    不同的对象，有不同的功能
    套接字对象种类也不一样，流式套接字，数据报套接字
    使用者决定的

    不同对象能够调用的方法不一样
    属性去实现，不同种类的套接字，就让你去能够调用不同的方法

    Process() 进程类怎么用 进程类的功能是单一的
    实例化对象----》功能单一，只有一种对象，就是进程对象
    固定的流程去实现指定的功能，Process()--start()--join()

    用户决定：使用进程干什么，怎么决定的？传参
    提供了继承，重写，使用起来更加灵活
    凡是用户去选择的，几乎都是传参数去决定的

3.  设计原则
    * 站在用户角度，想用法
    * 能够为用户实现的，不麻烦使用者
    * 不能替使用者决定的，提供接口(所谓的接口就是参数)让用户方便传递或者通过调用方法让用户决定
      让用户调用不同的方法做选择
    * 让功能更加的单一，不要把过多的功能掺杂到一个里面

4.  编写步骤：先搭框架，在实现具体业务逻辑

"""

from socket import *
from select import *

#  全局变量


HOST = '0.0.0.0'
PORT = 8889
ADDR = (HOST, PORT)

# 创建tcp套接字   是监听套接字
tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(5)

# 设置为非阻塞
tcp_socket.setblocking(False)

p = epoll()  # 建立epoll对象
p.register(tcp_socket, EPOLLIN)  # 初始监听对象,POLLIN是关注的事件，读事件

#  准备工作，建立文件描述符和IO对象对应的字典  时刻与register的IO一致
map = {tcp_socket.fileno(): tcp_socket}  # 以文件描述符为键，以对象为值

# 循环监听
while True:
    #  对关注的IO进行监控
    events = p.poll()  # ******注意：这里不改epoll，依然使用poll*******
    # events--->[(fileno,event),().....]  每个元组代表一个就绪的IO
    # 第一项是就绪IO的文件秒数符，第二项是事件
    for fd, event in events:  # 用两个变量去取这个值
        #  分情况讨论
        if fd == tcp_socket.fileno():  # 监听套接字的处理
            #  处理客户端连接
            connfd, addr = map[fd].accept()  # 接收来自客户端的连接，用IO对象
            print('Connect from', addr)
            connfd.setblocking(False)  # 设置非阻塞
            p.register(connfd, EPOLLIN | EPOLLERR)  # 添加到监控
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
            map[fd].send(b'OK')

