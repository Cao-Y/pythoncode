import serial
import serial.tools.list_ports
import time
import chardet
import socketserver
import socket


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

def recevemessage(ser):  #发送给控制板信息，并读取控制板传来的信息
    if ser:
        ser.write('c'.encode('utf-8'))
        time.sleep(0.05)
        allMessage = ser.read(ser.inWaiting())
        ser.flushInput()
        return allMessage
    else :
        return 0

def sendOrder(order):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # while flag:
    #     s.sendto(order.encode('utf-8'), ('192.168.31.20', 8080))
    s.sendto(order.encode('utf-8'), ('192.168.2.10', 8080))
    # while True:
    #     s.sendto(order.encode('utf-8'), ('192.168.31.20', 8000))
        #echo_back, address = s.recvfrom(1024)
        #print(address)
        #print(echo_back.decode('utf-8'))


if __name__ =="__main__":
    port = read_ports()
    ser = serial.Serial(port[0], 57600)
    time.sleep(1.0)
    while True:
        message = recevemessage(ser).decode()
        #print(message)
        if 'L1' in message :
            #sendOrder("a:x0500,y0500,z0500,0,0,0,0,0.")
            #print(message[4:19])
            num = message[4:19].split(",")
            if len(num)!=4:
                continue

            print(num[0])
            print(num[1])
            print(num[2])
            print(num[3])
        elif 'DOWN' in message:
            # print(message)
            sendOrder("a:x0200,y0500,z0500,0,0,0,0,0.")
        elif 'Up' in message :
            sendOrder("a:x0800,y0500,z0500,0,0,0,0,0.")
        elif 'LEFT' in message :
            sendOrder("a:x0500,y0800,z0500,0,0,0,0,0.")
        elif 'Right' in message :
            sendOrder("a:x0500,y0200,z0500,0,0,0,0,0.")
        elif 'L2' in message :
            sendOrder("a:x0500,y0500,z0800,0,0,0,0,0.")
        elif 'R2' in message :
            sendOrder("a:x0500,y0500,z0200,0,0,0,0,0.")
