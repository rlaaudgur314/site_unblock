import SocketServer
import socket

def CheckHTTPMethod(data):
    if(data.split(' ')[0] in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']):
        return True
    return False

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        buf = self.request.recv(8192)
        
        if CheckHTTPMethod(buf):
            #find host
            tmp = buf.split('Host: ')
            sockHost = tmp[1][0:tmp[1].find('\r\n')]
            
            
            dummy = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'
            buf = dummy + buf
            
            #send request
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((sockHost, 80))
            sock.sendall(buf)
            cnt = 0
            
            while(1):
                recvdata = sock.recv(8192)
                if not recvdata:
                    break
                #print(recvdata)
                if(recvdata.count('HTTP/1.1') == 2): # data together
                    recvdata = recvdata[recvdata[1:].find('HTTP/1.1'):] # second data
                    #print(recvdata)
                    self.request.sendall(recvdata)
                else:
                    if(cnt == 0): # drop first data
                        cnt = 1
                        continue
                    else:
                        cnt = 0
                        self.request.sendall(recvdata)

            print('end')
            sock.close()

if __name__ == '__main__':
    host, port = '127.0.0.1', 1234
    server = SocketServer.ThreadingTCPServer((host,port), MyTCPHandler)
    server.serve_forever()
  

