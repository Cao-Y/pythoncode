import socketserver
import socket
import serial
import serial.tools.list_ports
import time

def read_ports():
    """获取当下所有设备号"""
    all_ports = [ ]
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        return all_ports
    else:
        for ports in port_list:
            port_list_0 = ''.join(str(i) for i in list(ports)[0])
            all_ports.append(port_list_0)
        return all_ports


#class udpServer(socketserver.BaseRequestHandler):

    # def setup(self):
    #     port = read_ports()
    #     self.ser = serial.Serial(port[0], 9600)
    #     time.sleep(1.0)
#    def handle(self):
 #       global message
        # conn = self.request
        # print(conn)
        #print('获得连接：', self.client_address)
 #       client_data = self.request[0]
 #       if not client_data:
 #           print('断开连接')
        #print(client_data.decode('utf-8'))
  #      message = client_data.decode('utf-8')
        #print(message)
        # self.ser.write(message.encode('utf-8'))
        # time.sleep(0.05)
        # allMessage = self.ser.read(self.ser.inWaiting())
        # print(allMessage)
        # print('开始发送...')
        # self.request[1].sendto(client_data,self.client_address)

    # def finish(self):
    #     self.ser.close()

def sendMessage(serial,message):  #发送给控制板信息，并读取控制板传来的信息
    if serial:
        serial.write(message.encode('utf-8'))
        time.sleep(0.07)
        #allMessage = serial.read(ser.inWaiting())
        time.sleep(0.07)
        #return allMessage
    else :
        return 0

if __name__ == '__main__':
    myip = '192.168.2.10'   #gai
    myport1 = 8080  #gai
    bufsize = 65535 #gai
    udpClient1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #gai
    udpClient1.bind((myip, myport1))  #gai
    port = read_ports()   #gai
    if port:
        ser = serial.Serial(port[0],9600)  #读出端口
        time.sleep(3)
        time.sleep(1.0)
        #server = socketserver.UDPServer(("192.168.2.10", 8080), udpServer)  #使用处理单连接的UDPServer
        #server.handle_request() #gai
        while True:   #gai
            #server.handle_request()
            if not ser.isOpen():
                ser.close()
                port = read_ports()
                ser = serial.Serial(port[0],9600)  #读出端口
                time.sleep(1)
            msg, addr1=udpClient1.recvfrom(bufsize)
            message=msg.decode('utf-8')
            if message :
                mes = sendMessage(ser,message) #将收到的指令发给控制板
                
                print(message)
                print(mes)
                time.sleep(0.1)

    else :
        print("connect error")

