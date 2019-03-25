import serial
import serial.tools.list_ports
import threading
import time
import inspect
import ctypes


global update_port_name_control
update_port_name_control = True
global my_dev
my_dev = []
global thread_disk
thread_disk = {}
global wrong_log
wrong_log = []
global startall_control
startall_control = True


def read_ports():
    """获取当下所有设备号"""
    all_ports = []
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        return all_ports
    else:
        for ports in port_list:
            # print(list(ports))
            port_list_0 = ''.join(str(i) for i in list(ports)[0])
            # print(port_list_0)
            # ser = serial.Serial(port_list_0, 115200, timeout=60)
            # print("check which port was really used >", ser.name)
            all_ports.append(port_list_0)
        return all_ports


def update_port_name():
    """用来更新端口的线程程序"""
    while True:
        if update_port_name_control:
            my_dev = read_ports()
        time.sleep(0.1)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    """用来杀死线程"""
    _async_raise(thread.ident, SystemExit)


def tongyongkongzhiban(ser, name):
    try:
        thread_disk[name]['acontrol'] = []
        thread_disk[name]['k_a'] = False       #当k_a=True程序将acontrol内容发送到控制板中
        thread_disk[name]['dcontrol'] = []
        thread_disk[name]['k_d'] = False
        thread_disk[name]['econtrol'] = []
        thread_disk[name]['k_e'] = False
        thread_disk[name]['binformation'] = []
        thread_disk[name]['k_b'] = True       #当k_b=True程序将从控制板中读取传感器信息并保存到binformation内容发送到控制板中
        thread_disk[name]['cinformation'] = []
        thread_disk[name]['k_c'] = False
        while True:
            for key in sorted(thread_disk[name].keys()):
                if ('control' in key) and (thread_disk[name]['k_' + key[:key.find('control')]]):
                    ser.write((key[:key.find('control')] + thread_disk[name][key][-1]).encode('utf-8'))
                    thread_disk[name]['k_' + key[:key.find('control')]] = False
                if ('information' in key) and (thread_disk[name]['k_' + key[:key.find('information')]]):
                    ser.write(key[:key.find('information')].encode('utf-8'))
                    time.sleep(0.1)
                    thread_disk[name][key] = [ser.read(ser.inWaiting()).decode('utf-8')]
                    thread_disk[name]['k_' + key[:key.find('information')]] = False
    except:
        thread_disk[name]['wrong'].append('板子执行出现问题')
        print('板子执行出现问题', name)
        ser.close()
        """快速去除板子"""
        del thread_disk[name]
        print('设备', name, '已拔出')  #该方法可能出问题
    finally:
        ser.close()


def control_dev(name):
    """用于初始化设备信息并且确定设备的行为"""
    if type(name) == type([]):
        name=name[0]
    try:
        ser = serial.Serial(name, 115200)
    except serial.serialutil.SerialException:
        pass
    time.sleep(1)
    ser.write('b'.encode('utf-8'))
    time.sleep(0.1)
    ser.read(ser.inWaiting())
    # print(ser.name)
    try:
        if ser.write('b'.encode('utf-8')):
            time.sleep(0.1)
            if ser.inWaiting() == 0:
                if not ('与设备%s初始化通信失败' % name) in thread_disk[name]['wrong']:
                    thread_disk[name]['wrong'].append('与设备%s初始化通信失败' % name)
                    print('与设备%s初始化通信失败' % name)
                    raise NameError
                return False
            else:
                thread_disk[name]['description'] = [ser.read(ser.inWaiting()).decode('utf-8')]
                # print(self.thread_disk[name]['description'])
                """下面开始判断设备行为"""
                if 'tongyongkongzhiban' in thread_disk[name]['description'][0]:
                    print('与设备%s初始化通信成功' % name)
                    tongyongkongzhiban(ser, name)
    except Exception as e:
        #print(e)
        if not ('无法启动设备%s' % name) in thread_disk[name]['wrong']:
            thread_disk[name]['wrong'].append('无法启动设备%s' % name)
            print('无法启动设备：', name)
    finally:
        ser.close()


def startall():
    """此函数用于管理一切插上的串口设备"""
    while startall_control:
        try:
            my_ports = sorted(read_ports())
            my_threads = sorted(thread_disk.keys())
            #print(my_ports , my_threads)
            if my_ports != my_threads:
                for i in my_threads:
                    if not i in my_ports:
                        if thread_disk[i]['thread'].isAlive():
                           stop_thread(thread_disk[i]['thread'])
                        del thread_disk[i]
                        print('设备', i, '已拔出')
                for i in my_ports:
                    if not i in my_threads:
                        thread_disk[i] ={}
                        thread_disk[i]['thread'] = threading.Thread(target=control_dev, args=(i,))
                        print('设备', i, '是否加载成功？', thread_disk[i]['thread'].isAlive())
                        thread_disk[i]['wrong'] = []
                        thread_disk[i]['thread'].setDaemon(True)
                        thread_disk[i]['thread'].start()
                        print('设备', i, '是否加载成功？', thread_disk[i]['thread'].isAlive())
                        if not thread_disk[i]['thread'].isAlive():
                            del thread_disk[i]
                            continue
            for key in my_threads:
                if '板子执行出现问题' in thread_disk[key]['wrong']:
                    if thread_disk[key]['thread'].isAlive():
                        stop_thread(thread_disk[key]['thread'])
                    if not thread_disk[key] in wrong_log:
                        wrong_log.append(thread_disk[key])
                    del thread_disk[key]
        except Exception as e:
            #print(e)
            continue


def lets_start():
    rex = threading.Thread(target=startall, args=())
    rex.setDaemon(True)
    rex.start()
    kk = False
    while True:
        try:
            time.sleep(1)
            #print('key:', sorted(thread_disk.keys()))
            for key in sorted(thread_disk.keys()):
                #print(sorted(thread_disk.keys()))
                if not thread_disk[key]['k_b'] and not kk:
                    thread_disk[key]['k_b']=True
                    kk=True
                if not thread_disk[key]['k_b'] and kk:
                    print(thread_disk[key]['binformation'],key)
                    kk=False
        except :
            continue






