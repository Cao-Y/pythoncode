import serial
import time
a=serial.Serial('/dev/ttyUSB2',115200)
i=1
print('b'.encode('utf-8').decode('gbk'))
while i<2:
    a.write('b'.encode('utf-8'))
    time.sleep(1)
    print(a.name,a.inWaiting())
    print(a.read(a.inWaiting()).decode('utf-8'))
    i+=1
    time.sleep(0.1)