import time
import serial
import serial.tools.list_ports


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


def message(command,ser):  #发送给控制板信息，并读取控制板传来的信息
    #time.sleep(1.0)
    ser.write(command.encode('utf-8'))
    time.sleep(1)
    allMessage =ser.read(ser.inWaiting())
    return allMessage

def recevemessage(all_ports): #发送给控制板信息，并读取控制板传来的信息
    number = all_ports
    ser = serial.Serial(number[0], 9600)
    return ser

if __name__ == "__main__":
    port = read_ports()
    ser = recevemessage(port)
    time.sleep(5.4)
    while True:
        command = input()
        mes = message(command,ser)
        print(mes)

