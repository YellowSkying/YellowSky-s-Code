"""
在线词典：服务器
"""
from socket import *
from select import select
import pymysql


class DataBases:
    def __init__(self):
        self.args = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "123456",
            "database": "dict",
            "charset": "utf8"
        }
        self.db = pymysql.connect(**self.args)
        self.cur = self.db.cursor()
        self.sql_register = "insert into user (user_name,password) values (%s,%s);"
        self.sql_login = "select password from user where user_name=%s;"
        self.sql_get_nid = "select id from user where user_name=%s;"
        self.sql_whistory = "insert into history (word,user_id) values (%s,%s);"
        self.sql_look_up = "select mean from words where word=%s;"
        self.sql_rhistory = "select word,time from history where user_id=%s order by id desc limit 10;"

    def register(self, username, password):
        try:
            self.cur.execute(self.sql_register, (username, password))
            self.db.commit()
        except:
            return False
        else:
            return True

    def close(self):
        self.cur.close()
        self.db.cursor()

    def login(self, name):
        self.cur.execute(self.sql_login, (name,))
        res = self.cur.fetchone()
        if res:
            return res[0]

    def look_up(self, word, name):
        self.cur.execute(self.sql_get_nid, (name,))
        nid = self.cur.fetchone()[0]
        self.cur.execute(self.sql_whistory, (word, nid))
        self.db.commit()
        self.cur.execute(self.sql_look_up, (word,))
        res = self.cur.fetchone()
        if res:
            return res[0]

    def get_history(self, name):
        self.cur.execute(self.sql_get_nid, (name,))
        nid = self.cur.fetchone()[0]
        self.cur.execute(self.sql_rhistory, (nid,))
        res = self.cur.fetchall()
        if res:
            return res


class Server:
    def __init__(self, host="0.0.0.0", port=8888):
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
            rs, ws, xs = select(rlist, wlist, xlist)
            for event in rs:
                if event is self.tcp_socket:
                    connfd, addr = self.tcp_socket.accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    rlist.append(connfd)
                else:
                    data = event.recv(1024)
                    if not data:
                        rlist.remove(event)
                        event.close()
                        print("Unconnect type02")
                        continue
                    msg = data.decode().split(" ", 2)
                    if msg[0] == "REGISTER":
                        self.register(event, msg[1], msg[2])
                    elif msg[0] == "LOGIN":
                        self.login(event, msg[1], msg[2])
                    elif msg[0] == "DICT":
                        self.look_up(event, msg[1], msg[2])
                    elif msg[0] == "HISTORY":
                        self.get_history(event, msg[1])
                    elif msg[0] == "EXIT":
                        rlist.remove(event)
                        event.close()
                        print("Unconnect type01")

    def register(self, connfd, name, pw):
        if self.db.register(name, pw):
            connfd.send(b"OK")
        else:
            connfd.send(b"NO")

    def login(self, connfd, name, pw):
        res = self.db.login(name)
        if res:
            if res == pw:
                connfd.send(b"OK")
            else:
                connfd.send(b"NO")
        else:
            connfd.send(b"NO")

    def look_up(self, connfd, word, name):
        res = self.db.look_up(word, name)
        if res:
            connfd.send(res.encode())
        else:
            connfd.send(b"Not found,sorry...")

    def get_history(self, connfd, name):
        res = self.db.get_history(name)
        if res:
            data = str(res)
            connfd.send(data.encode())
        else:
            connfd.send(b"NO")

    def start(self):
        self.tcp_socket.listen(10)
        self.IO_listening()


if __name__ == '__main__':
    server = Server()
    server.start()
