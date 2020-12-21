"""
在线词典：服务器
"""
from socket import *
from select import select
import pymysql

class DataBases:
    def __init__(self):
        self.args = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"123456",
    "database":"dict",
    "charset":"utf8"
}
        self.db = pymysql.connect(**self.args)
        self.cur = self.db.cursor()
        self.sql_register = "insert into user (user_name,password) values (%s,%s);"

    def register(self,username,password):
        try:
            self.cur.execute(self.sql_register, (username,password))
            self.db.commit()
        except:
            return False
        else:
            return True

    def close(self):
        self.cur.close()
        self.db.cursor()



class Server:
    def __init__(self,host="0.0.0.0",port=8888):
        self.db = DataBases()
        self.ADDR = (host, port)
        self.tcp_socket = self.create_socket()

    def create_socket(self):
        sock = socket()
        sock.bind(self.ADDR)
        sock.setblocking(False)
        return sock

    def IO_listening(self):
        rlist = [self.tcp_socket]
        wlist = []
        xlist = []
        while True:
            rs,ws,xs = select(rlist,wlist,xlist)
            for event in rs:
                if event is self.tcp_socket:
                    connfd,addr = self.tcp_socket.accept()
                    print("Connect from",addr)
                    connfd.setblocking(False)
                    rlist.append(connfd)
                else:
                    data = event.recv(1024).decode().split(" ",2)
                    if data[0] == "REGISTER":
                        name = data[1]
                        pw = data[2]
                        if self.db.register(name,pw):
                            event.send(b"OK")
                            break
                        event.send(b"NO")


    def start(self):
        self.tcp_socket.listen(10)
        self.IO_listening()



if __name__ == '__main__':
    server = Server()
    server.start()