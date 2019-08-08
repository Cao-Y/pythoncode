import serial
import serial.tools.list_ports
import time
import cv2
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
    from jiance import zhuizong
    # 打开摄像头
    from client import receiveVideo

    port = read_ports()
    ser = serial.Serial(port[0], 57600)
    time.sleep(1.0)
    while True:
        img = receiveVideo()
        cv2.imshow('video',img)
        cv2.waitKey(1)
        message = recevemessage(ser).decode()
        #print(message)
        if 'L1' in message :
            #sendOrder("a:x0500,y0500,z0500,0,0,0,0,0.")
            #print(message[4:19])
            num = message[4:19].split(",")
            if len(num)!=4:
                continue
            if int(num[3])>128:
              sendOrder("a:x"+num[0]+",y"+num[1]+",z"+num[2]+",r,0,0,0,0.")
              #print("a:x"+num[0]+",y"+num[1]+",z"+num[2]+",r,0,0,0,0.")
            elif int(num[3])<128:
              sendOrder("a:x" + num[0] + ",y" + num[1] + ",z" + num[2] + ",l,0,0,0,0.")
              #print("a:x"+num[0]+",y"+num[1]+",z"+num[2]+",l,0,0,0,0.")
            elif int(num[3]) == 128:
              sendOrder("a:x" + num[0] + ",y" + num[1] + ",z" + num[2] + ",0,0,0,0,0.")
              print("a:x" + num[0] + ",y" + num[1] + ",z" + num[2] + ",0,0,0,0,0.")
        elif 'LEFT' in message:
            # print(message)
            sendOrder("h1")   #左滚转
        elif 'Right' in message :
            sendOrder("h2")   #右滚转
        elif 'Square' in message :
            sendOrder("i")    #紧急上浮
        elif 'X just changed' in message :
            sendOrder("j")    #贴附模式
        elif 'Up' in message :
            sendOrder("g:+")
        elif 'DOWN' in message :
            sendOrder("g:-")
        elif 'L2' in message :
            sendOrder("k1")
        elif 'R2' in message:
            sendOrder("k2")
        elif 'Circle' in message :
            print("进入跟踪模式")
            while True:
                img = receiveVideo()
                cv2.imshow('video', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                center,s = zhuizong(img)
                if center == None and s == 0:
                    continue
                s=str(s)
                center1 =str(center[0])
                #print(center)
                #print(s)
                # sendOrder("l:x"+ +",s"+ +".")
                print("l:x"+center1+",s"+s+".")
                time.sleep(0.1)
                sendOrder("l:x" + center1 + ",s" + s + ".")
                message = recevemessage(ser).decode()
                ser.flushInput()
                if 'Circle' in message :
                    print("退出跟踪模式")
                    break
