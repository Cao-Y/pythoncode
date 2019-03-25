import serial
import serial.tools.list_ports

port_list = list(serial.tools.list_ports.comports())
print(port_list)

if len(port_list) <= 0:
    print("The Serial port can't find!")

else:
    for ports in port_list:
        print(list(ports))
        port_list_0=''.join(str(i) for i in list(ports)[0])
        print(port_list_0)
        ser = serial.Serial(port_list_0, 115200, timeout=60)
        print("check which port was really used >", ser.name)
