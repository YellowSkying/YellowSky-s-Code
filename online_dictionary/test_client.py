from socket import *
import datetime

ADDR = ('127.0.0.1',8888)
tcp_socket = socket()
tcp_socket.connect(ADDR)

# 用户注册测试
# while True:
#     name = input("请输入用户名：")
#     pw = input("请输入密码：")
#     if not pw:
#         print("密码不能为空！")
#         continue
#     data = "REGISTER "+name+" "+pw
#     tcp_socket.send(data.encode())
#     res = tcp_socket.recv(1024)
#     if res == b"OK":
#         break
#     print("用户名已经被注册")

# 用户登录测试
# while True:
#     name = input("请输入用户名：")
#     pw = input("请输入密码：")
#     data = "LOGIN "+name+" "+pw
#     tcp_socket.send(data.encode())
#     res = tcp_socket.recv(1024)
#     if res == b"OK":
#         print("登陆成功")
#         break
#     print("用户名或密码错误")

# 用户查询单词测试：
# name = input("请输入用户名：")
# word = input("请输入单词：")
# data = "DICT "+word+" "+name
# tcp_socket.send(data.encode())
# res = tcp_socket.recv(1024)
# print(res.decode())

# 查找历史记录
name = input("请输入用户名：")
data = "HISTORY "+"Harry"
tcp_socket.send(data.encode())
res = tcp_socket.recv(1024)
res = eval(res.decode())
print("==========history==========")
for word,time in res:
    print(str(time)+"查询了"+word)
print("===========================")

tcp_socket.send(b"EXIT")
tcp_socket.close()

# while True:
#     pw = input("请输入密码：")
#     if not pw:
#         print("密码不能为空！")
#         continue
#     tcp_socket.send(pw.encode())
#     break


