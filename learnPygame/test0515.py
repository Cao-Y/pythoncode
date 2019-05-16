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
        ser.write('a:x0200,y0500,z0500,0,0,0,0,0.'.encode())
        time.sleep(3.5)
        allMessage = ser.read(ser.inWaiting())
        return allMessage
    else :
        return 0


if __name__ =="__main__":
    port = read_ports()
    ser = serial.Serial(port[0], 9600)
    time.sleep(1)
    while True:
        message = recevemessage(ser)
        message = message.decode()
        print(message)