import socketserver
import serial
import serial.tools.list_ports
import time
global message

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
    def handle(self):
        global message
        print('服务端启动...')
        # conn = self.request
        # print(conn)
        print('获得连接：', self.client_address)
        client_data = self.request[0]
        if not client_data:
            print('断开连接')
        print(client_data.decode('utf-8'))
        message = client_data.decode('utf-8')

        # print('开始发送...')
        # self.request[1].sendto(client_data,self.client_address)

def sendMessage(ser):  #发送给控制板信息，并读取控制板传来的信息
    if ser:
        ser.write(message.encode('utf-8'))
        time.sleep(0.05)
        allMessage = ser.read(ser.inWaiting())
        return allMessage
    else :
        return 0

if __name__ == '__main__':
    port = read_ports()
    ser = serial.Serial(port[0], 57600)
    server = socketserver.UDPServer(("192.168.31.20", 8000), udpServer)  #使用处理单连接的UDPServer
    server.serve_forever()
    mes = sendMessage(ser)
    print(mes)