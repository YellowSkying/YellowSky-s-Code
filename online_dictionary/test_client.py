from socket import *

ADDR = ('127.0.0.1',8888)
tcp_socket = socket()
tcp_socket.connect(ADDR)

while True:
    name = input("请输入用户名：")
    pw = input("请输入密码：")
    if not pw:
        print("密码不能为空！")
        continue
    data = "REGISTER "+name+" "+pw
    tcp_socket.send(data.encode())
    res = tcp_socket.recv(1024)
    if res == b"OK":
        break

# while True:
#     pw = input("请输入密码：")
#     if not pw:
#         print("密码不能为空！")
#         continue
#     tcp_socket.send(pw.encode())
#     break