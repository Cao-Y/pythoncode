import socketserver
import serial
import serial.tools.list_ports
import time

def read_ports():
    """获取当下所有设备号"""
    all_ports = []
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        return all_ports
    else:
        for ports in port_list:
            port_list_0 = ''.join(str(i) for i in list(ports)[0])
            all_ports.append(port_list_0)
        return all_ports


class udpServer(socketserver.BaseRequestHandler):

    # def setup(self):
    #     port = read_ports()
    #     self.ser = serial.Serial(port[0], 9600)
    #     time.sleep(1.0)
    def handle(self):
        global message
        # conn = self.request
        # print(conn)
        print('获得连接：', self.client_address)
        client_data = self.request[0]
        if not client_data:
            print('断开连接')
        #print(client_data.decode('utf-8'))
        message = client_data.decode('utf-8')
        print(message)
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
        allMessage = serial.read(ser.inWaiting())
        return allMessage
    else :
        return 0

if __name__ == '__main__':
    port = read_ports()
    if port:
        ser = serial.Serial(port[0], 9600)
        #time.sleep(1.0)
        server = socketserver.UDPServer(("192.168.31.20", 8080), udpServer)  #使用处理单连接的UDPServer
        while True :
            server.handle_request()
            if message :
                mes = sendMessage(ser, message)
                print(mes)

    else :
        print("connect error")


