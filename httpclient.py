#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split(" ", 2)[1]
        return code

    def get_headers(self,data):
        header = data.split("\r\n\r\n")[0]
        return header

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def get_url(self, url):
        url = url.strip("http://")
        url = url.split("/", 1)
        dest = url[0].split(":")

        #result = urlparse(url)


        #print("Url Host: "+dest[0]+"\r\n")
        #print("Url Port: "+dest[1]+"\r\n")
        #print("Url Path: "+url[1]+"\r\n")

        return dest[0], dest [1], url[1]
        #return result.hostname, result.port, result.path
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        print("Url: "+url+"\r\n")

        host, port, path = self.get_url(url)
        print("GET Host: "+host+"\r\n")
        print("GET Port: "+port+"\r\n")
        print("GET Path: "+path+"\r\n")

        sock = self.connect(host, int(port))

        request = "GET /" + path + " HTTP/1.1\r\nHost: " + host
        print("GET Request: "+request+"\r\n")
        print("before sendall\r\n")
        sock.sendall(bytes(request.encode(), "utf-8"))
        print("after sendall\r\n")
        response = self.recvall(self.sock)
        print("GET Response: "+response+"\r\n")

        sock.close()

        print("GET response: "+response)
        code = self.get_code()
        print("GET code: "+code)
        header = self.get_headers()
        print("GET header"+header)
        body = self.get_body()
        print("Get body: "+body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        print("POST Url: "+url+"\r\n")

        host, port, path = self.get_url(url)
        sock = self.connect(host, int(port))

        request = "POST " + path + " HTTP/1.1\r\nHost: " + host
        print("POST Request: "+request+"\r\n")
        print("before sendall\r\n")
        sock.sendall(bytes(request.encode(), "utf-8"))
        print("after sendall\r\n")
        response = self.recvall(self.sock)

        sock.close()

        print("POST Response: "+response+"\r\n")
        code = self.get_code()
        print("POST Code: "+code+"\r\n")
        header = self.get_headers()
        print("POST Header: "+ header+"\r\n")
        body = self.get_body()
        print("POST Body: "+body+"\r\n")
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
