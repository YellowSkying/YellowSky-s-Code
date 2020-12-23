"""
客户端代码
"""
from socket import *
import datetime

ADDR = ("127.0.0.1",8888)

class DictClientController:
    def __init__(self, host, port):
        self.ADDR = (host, port)
        self.tcp_socket = self.create_socket()

    def create_socket(self):
        sock = socket()
        sock.connect(self.ADDR)
        sock.setblocking(True)
        return sock

    def close(self):
        self.tcp_socket.send(b"EXIT")
        self.tcp_socket.close()

    def login(self, name, pw):
        data = "LOGIN " + name + " " + pw
        self.tcp_socket.send(data.encode())
        res = self.tcp_socket.recv(1024)
        if res == b"OK":
            return True

    def look_up(self, word, name):
        data = "DICT " + word + " " + name
        self.tcp_socket.send(data.encode())
        res = self.tcp_socket.recv(1024)
        return res.decode()

    def get_history(self, name):
        data = "HISTORY " + name
        self.tcp_socket.send(data.encode())
        res = self.tcp_socket.recv(1024)
        return res.decode()

    def register(self, name, pw):
        data = "REGISTER " + name + " " + pw
        self.tcp_socket.send(data.encode())
        res = self.tcp_socket.recv(1024)
        if res == b"OK":
            return True


class DictClientView:
    def __init__(self,host='127.0.0.1', port=8888):
        self.controller = DictClientController(host=host, port=port)
        self.name = ""

    def display_first_menu(self):
        print("-----欢迎使用在线词典!-----")
        print("1,登录")
        print("2,注册")
        print("3,退出")

    def display_second_menu(self):
        print("----------查字典----------")
        print("1,查单词")
        print("2,历史记录")
        print("3,注销")

    def select_first_menu(self):
        while True:
            self.display_first_menu()
            choice = input("请输入您的选择")
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                self.controller.close()
                print("感谢您使用在线词典,再见！")
                break
            else:
                print("输入无效指令")

    def login(self):
        while True:
            self.name = input("请输入用户名(不输入用户名返回上一级)：")
            if not self.name:
                break
            pw = input("请输入密码：")
            res = self.controller.login(self.name,pw)
            if res:
                print("登陆成功")
                self.select_second_menu()
                break
            print("用户名或密码错误")

    def register(self):
        while True:
            name = input("请输入用户名：")
            pw = input("请输入密码：")
            if not (pw and name):
                print("用户名密码不能为空！")
                continue
            if self.controller.register(name,pw):
                print("注册成功！")
                choice = input("输入1返回上级,输入其他进入查字典界面")
                if choice == "1":
                    break
                self.name = name
                self.select_second_menu()
            else:
                print("用户名已经被注册")

    def select_second_menu(self):
        while True:
            self.display_second_menu()
            choice = input("请输入您的选择")
            if choice == "1":
                self.look_up()
            elif choice == "2":
                self.get_history()
            elif choice == "3":
                self.name = ""
                break
            else:
                print("输入无效指令")

    def look_up(self):
        while True:
            word = input("请输入单词(不输入返回上级)：")
            if not word:
                break
            res = self.controller.look_up(word,self.name)
            print("解释：" + res)

    def get_history(self):
        res = self.controller.get_history(self.name)
        if res == "NO":
            print("No history...")
        else:
            res = eval(res)
            print("==========history==========")
            for word,time in res:
                print(str(time)+"查询了"+word)
            print("===========================")

    def main(self):
        self.select_first_menu()


if __name__ == '__main__':
    client = DictClientView()
    client.main()
