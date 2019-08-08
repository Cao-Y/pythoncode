import socket
import serial
import serial.tools.list_ports
import time

def read_ports():
    all_ports=[ ]
    port_list=list(serial.tools.list_ports.comports())
    if len(port_list)<=0:
        return all_ports
    else:
       for ports in port_list:
            port_list_0=' '.join(str(i) for i in list(ports)[0])
            all_ports.append(port_list_0)
            return all_ports
# class udpSever(sockersever.BaseRequestHandler):
#     #def setup(self)
#     #port=read_ports()
#     #self.ser=serial.Serial(port[0],9600)
#     time.sleep(1.0)
#     def handle(self):
#         global message
#        #conn=self.request
#         print('获得连接')
#        #print('获得连接:',self.client_address)
#     client_data=self.request[0]
#     if not client_data:
#         print('断开连接')
#     #print(client_data,decode('utf-8'))
#     #print(message)
#     #self.ser.write(message.encode('utf-8'))
#     #time.sleep(0.05)
#     #allMessage=self.ser.read(self.ser.inWaiting())
#     #print(allMessage)
#     #print("开始发送。。。")
#     #self.request[1].sendto(client_data,self.client_address)
#     #def finish(self)
#     #self.ser.close()

def sendMessage(serial,message):
    if serial:
        serial.write(message.encode('utf-8'))
        time.sleep(0.07)
        return 1
    else:
        return 0


if __name__ == '__main__':
    myip = '192.168.2.10'   #改
    myport1 = 8080   #改
    bufsize = 65535   #改
    udpClient1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #改
    udpClient1.bind((myip,myport1))   #改
    port=read_ports()   #改
    if port:
        ser=serial.Serial(port[0],9600)
        time.sleep(3)
        time.sleep(1.0)
    #server.handle_request()        改
    while True:   #改
        if not ser.isOpen():
            ser.close()
            port = read_ports()
            ser = serial.serial(port[0],9600)
            time.sleep(1)
        msg, addr1 = udpClient1.recvfrom(bufsize)   #改
        message = msg.decode('utf-8')   #改
        if message :
           mes = sendMessage(ser,message)
           print(message)
           print(mes)
           time.sleep(0.1)
        else:
            print("connect error")