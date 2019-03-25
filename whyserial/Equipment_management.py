import serial
import serial.tools.list_ports
import threading
import time
import inspect
import ctypes


class equipmentManagement:




    def read_ports(self):
        """获取当下所有设备号"""
        all_ports=[]
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            return all_ports
        else:
            for ports in port_list:
                #print(list(ports))
                port_list_0 = ''.join(str(i) for i in list(ports)[0])
                #print(port_list_0)
                #ser = serial.Serial(port_list_0, 115200, timeout=60)
                #print("check which port was really used >", ser.name)
                all_ports.append(port_list_0)
            return all_ports

    def update_port_name(self):
        """用来更新端口的线程程序"""
        while self.update_port_name_control:
            self.my_dev = self.read_ports()
            time.sleep(1)

    def _async_raise(self, tid, exctype):
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

    def stop_thread(self, thread):
        """用来杀死线程"""
        self._async_raise(thread.ident, SystemExit)

    def tongyongkongzhiban(self, ser, name):
        try:
            self.thread_disk[name]['acontrol'] = []
            self.thread_disk[name]['k_a'] = False
            self.thread_disk[name]['dcontrol'] = []
            self.thread_disk[name]['k_d'] = False
            self.thread_disk[name]['econtrol'] = []
            self.thread_disk[name]['k_e'] = False
            self.thread_disk[name]['binformation'] = []
            self.thread_disk[name]['k_b'] = True
            self.thread_disk[name]['cinformation'] = []
            self.thread_disk[name]['k_c'] = False
            while True:
                for key in sorted(self.thread_disk[name].keys()):
                    if ('control' in key) and (self.thread_disk[name]['k_' + key[:key.find('control')]]):
                        ser.write((key[:key.find('control')] + self.thread_disk[name][key][-1]).encode('utf-8'))
                        self.thread_disk[name]['k_' + key[:key.find('control')]] = False
                    if ('information' in key) and (self.thread_disk[name]['k_' + key[:key.find('information')]]):
                        ser.write(key[:key.find('information')].encode('utf-8'))
                        time.sleep(0.1)
                        self.thread_disk[name][key] = [ser.read(ser.inWaiting()).decode('utf-8')]
                        self.thread_disk[name]['k_' + key[:key.find('information')]] = False

        except:
            self.thread_disk[name]['wrong'].append('板子执行出现问题')
            print('板子执行出现问题', name)
            ser.close()
        finally:
            ser.close()



    def control_dev(self, name):
        """用于初始化设备信息并且确定设备的行为"""
        ser = serial.Serial(name, 115200)
        time.sleep(1)
        ser.write('b'.encode('utf-8'))
        time.sleep(0.1)
        ser.read(ser.inWaiting())
        #print(ser.name)
        try:
            if ser.write('b'.encode('utf-8')):
                time.sleep(0.1)
                if ser.inWaiting() == 0:
                    if not ('与设备%s初始化通信失败' % name) in self.thread_disk[name]['wrong']:
                        self.thread_disk[name]['wrong'].append('与设备%s初始化通信失败' % name)
                        print('与设备%s初始化通信失败' % name)
                        raise NameError
                    return False
                else:
                    self.thread_disk[name]['description'] = [ser.read(ser.inWaiting()).decode('utf-8')]
                    #print(self.thread_disk[name]['description'])
                    """下面开始判断设备行为"""
                    if 'tongyongkongzhiban' in self.thread_disk[name]['description'][0]:
                        print('与设备%s初始化通信成功' % name)
                        self.tongyongkongzhiban(ser, name)
        except:
            if not ('无法启动设备%s' % name) in self.thread_disk[name]['wrong']:
                self.thread_disk[name]['wrong'].append('无法启动设备%s' % name)
                print('无法启动设备：', name)
        finally:
            ser.close()


    def startall(self):
        """此函数用于管理一切插上的串口设备"""
        while self.startall_control:
            my_ports = sorted(self.read_ports())
            my_threads=sorted(self.thread_disk)
            #print(my_ports,my_threads)
            if my_ports != my_threads:
                for i in my_threads:
                    if not i in my_ports:
                        if self.thread_disk[i]['thread'].isAlive():
                            self.stop_thread(self.thread_disk[i]['thread'])
                        del self.thread_disk[i]
                for i in my_ports:
                    if not i in my_threads:
                        self.thread_disk[i] ={}
                        self.thread_disk[i]['thread'] = threading.Thread(target=self.control_dev, args=(i,))
                        self.thread_disk[i]['wrong'] = []
                        self.thread_disk[i]['thread'].setDaemon(True)
                        self.thread_disk[i]['thread'].start()
            for key in my_threads:
                if '板子执行出现问题' in self.thread_disk[key]['wrong'] :
                    if self.thread_disk[key]['thread'].isAlive():
                        self.stop_thread(self.thread_disk[key]['thread'])
                    if not self.thread_disk[key] in self.wrong_log:
                        self.wrong_log.append(self.thread_disk[key])

                    del self.thread_disk[key]
            time.sleep(1)

    def __init__(self,thread_disk,my_dev,wrong_log):
        self.my_dev = my_dev#[]
        self.update_port_name_control = True
        self.startall_control = True
        self.thread_disk = thread_disk#{}
        self.wrong_log = wrong_log#[]
        print(1)
        self.startall()


def hh(thread_disk,my_dev,wrong_log):
    print(1)
    test1=equipmentManagement(thread_disk,my_dev,wrong_log)




if __name__== '__main__':
    my_dev=[]
    thread_disk={}
    wrong_log=[]
    kk=False
    test1=threading.Thread(target=hh, args=(thread_disk,my_dev,wrong_log,))
    test1.setDaemon(True)
    print(test1.isAlive())
    while True:
        time.sleep(2)
        print('key:', sorted(thread_disk.keys()))
        for key in sorted(thread_disk.keys()):

            try:
                print(sorted(thread_disk.keys()))
                if not thread_disk[key]['k_b'] and not kk:
                    thread_disk[key]['k_b']=True
                    kk=True
                if not thread_disk[key]['k_b'] and kk:
                        print(thread_disk[key]['binformation'],key)
                        time.sleep(1)
            except:
                continue









