"""
基于select 的IO 多路复用并发模型
重点代码！！！
"""



from socket import *
from select import select

#  全局变量

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)

# 创建套接字
tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(5)


#设置为非阻塞
tcp_socket.setblocking(False)

#  IO对象监控列别哦
rlist = [tcp_socket]  # 初始监听对象
wlist = []
xlist = []

# 循环监听
while True:
    # print(rlist)
    #  对关注的IO进行监控
    rs, ws, xs = select(rlist, wlist, xlist)
    #  对返回值rs   分情况讨论   监听套接字    客户端连接套接字
    for r in rs:
        if r is tcp_socket:   #  判断对象是否是一类对象,用is
            #  处理客户端连接
            connfd, addr = r.accept()
            print('Connect from', addr)
            connfd.setblocking(False)   #  设置为非阻塞
            rlist.append(connfd)        #  添加到监控列表
        else:
            # 收消息
            data = r.recv(1024)
            if not data:
                #客户端退出
                rlist.remove(r)  #移除对这个退出的客户端的关注
                r.close()
                continue  #这里使用continue，是因为这是在for循环里，如果有一个客户端退出了，此时break，其他的就都无法执行了，第一个退出了，继续取后面的
            print(data.decode())
            # r.send(b'OK')
            wlist.append(r)  # 不回复了,放入写列表,

    for w in ws:
        w.send(b'OK')  # 发送消息
        wlist.remove(w)  #  如果不移除，会不断的写

    # connfd, addr = rs[0].accept()
    # print('Connect from', addr)
    # rlist.append(connfd)


# wlist  主动发送，主动写入的作用


