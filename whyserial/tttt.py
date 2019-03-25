import serial
import easygui

ser = serial.Serial()
ser.baudrate = 9600  # 设置波特率（这里使用的是stc89c52）
ser.port = 'COM16'  # 端口是COM3
ser.timeout=0.5
print(ser)
ser.open()  # 打开串口
print(ser.is_open)  # 检验串口是否打开

while (1):
    Yes_or_No = easygui.buttonbox("是否良品?", choices=['Yes', 'No', '退出'])  # 提供简易UI
    if Yes_or_No == '退出': break
    if Yes_or_No == 'Yes':
        demo = '1'.encode()  # 传入2的ASCII码 这里用b+str强制转换
    else:
        demo = '0'.encode()  # 传入1的ASCII码 这里用b+str强制转换

    ser.write(demo)
    s = ser.readline().decode()
    # s = ser.read(1).decode()
    print(s)
