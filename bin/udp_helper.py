# UDP Class for handling comms
import socket
import time

class UDPComms(object):
    def __init__(self,ip='127.0.0.1',remoteport=8001,localport=8000,timeout=.01):
        self.ip = ip
        self.remoteport = remoteport
        self.localport = localport
        self.sock_local = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.sock_remote = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.sock_remote.bind((self.ip,self.remoteport))
        self.sock_remote.settimeout(timeout)

    def receive(self):
        now = time.time()
        while True:
            try:
                data, addr = self.sock_remote.recvfrom(1024)
                return data
            except Exception as inst:
                return inst
    def send(self,message):
        self.sock_local.sendto(message, (self.ip, self.localport))
