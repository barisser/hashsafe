import hashlib
import time
import math
import random
import socket
import sys
from thread import *
import threading
from bitcoin import *

elementlength=1000 #max number per array element, not number of elements
vectorlength=32  #number of elements per vector
neighbormax=10

homeip='71.198.63.116'

max_neighbors=10
timelistening=100

active=True

"""
def generate_private_public(text):  #text adds randomness only, not deterministic
    keysum=str(time.time()*1000000)+str(random.random()*1000)+text
    secret_exponent=hashlib.sha256(keysum).hexdigest()
    pub=keyToAddr(secret_exponent)
    priv=privateKeyToWif(secret_exponent)
    return priv,pub
"""
class node:

    def __init__(self, listeningport):
        timestamp=time.time()
        self.listeningport=listeningport
        self.timestamp=timestamp
        self.hashid=hashlib.sha256(str(timestamp+random.random()*1000000)).hexdigest()
        inth=int(self.hashid,16)
        self.hashvector=[0]*vectorlength
        self.neighbors=[[-1,'',8888]]*max_neighbors   #list of 2 element arrays of HASHID, IP ADDRESS, AND THEIR PORT

        r=0
        while inth>0:
            self.hashvector[r]=int(inth%elementlength)
            inth=inth/elementlength
            r=r+1
        self.sockets=[0]*(max_neighbors+1) #first socket should be SERVER socket

        #listening socket
        self.sockets[0]=self.create_socket('',self.listeningport)
        #self.create_socket('',listeningport,0)





    def create_socket(self, HOST, PORT):    #RETURNS SOCKET OBJECT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'

        #Bind socket to local host and port
        try:
            s.bind((HOST, PORT))
            #self.sockets[socketn]=s
            return s
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]



    def client_thread(self, connection):  #Whatever this node does as a SERVER
        #while True:
        data=connection.recv(1024)
        print "\nSERVER RECEIVING DATA: "+"\n"+str(data)
        reply=str(self.hashid)+"\n"+str(self.neighbors)
        print "\nSERVER REPLYING\n"
        connection.sendall(reply)
        connection.close()
        print "here"

    def message(self, host, port, message): #socket must be set up

        remote_ip=socket.gethostbyname(host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((remote_ip , port))
            #message = "GET / HTTP/1.1\r\n\r\n"
        s.sendall(message)
        print "MESSAGE SENT \n"
        reply = s.recv(4096)

        print "SERVER REPLY:"+"\n"+str(reply)

    def serve(self):
        j=0
        while active:
            j=j+1

            connection,address=self.sockets[0].accept()
            print j
            k=threading.Thread(target=self.client_thread,args=(connection,))
            k.daemon=True
            k.start()
            #self.client_thread(connection)
            print "Connected with "+str(address[0])+":"+str(address[1])

    def chat(self):
        for x in self.neighbors:
            m="my name is: "+str(self.hashid)
            h=x[1]
            p=x[2]
            self.message(h,p,m)


    def online(self):

        #SETUP A REPLYING SERVER
        self.sockets[0].listen(max_neighbors)
        print 'Socket now listening'
        active=True

        g=threading.Thread(target=self.serve)
        g.daemon=True
        g.start()



        r=threading.Thread(target=self.chat)

        r.daemon=True
        r.start()








def nodedistance(nodeavector,nodebvector):
    d=0
    if len(nodeavector)==len(nodebvector):
        a=0
        while a<len(nodeavector):
            d=d+(nodeavector[a]-nodebvector[a])*(nodeavector[a]-nodebvector[a])

            a=a+1
        #print d
        d=math.pow(float(d),0.5)
        return d
    else:
        return -1





a=node(8825)
#a.online()
