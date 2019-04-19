# -*- coding: utf-8 -*-
import pygame
from pygame import joystick
from pygame.locals import *

pygame.init()
joystick.init()
joy_count = joystick.get_count()

if joystick.get_init() == True:
    print("手柄模块初始化")
    joysticks = [joystick.Joystick(i) for i in range(joy_count)]
    print(joysticks)
    for i in range(joy_count):
        joy = joysticks[i]
        joy.init()
        if joy.get_init() == True :
            print("手柄连接成功")
            name = joy.get_name()
            print(name)
            while 1:
                for event in pygame.event.get():
                    print(event)
                    if event.type == JOYBUTTONDOWN: #获取按键
                        print(event.__dict__)
                        print(event.joy)
                        print(event.button)
                    if event.type == JOYAXISMOTION: #获取摇杆
                        print(event.__dict__)
                        print(event.joy)
                        print(event.axis)
                        print(event.value)
                    if event.type == JOYHATMOTION :#获取hat
                        print(event.__dict__)
                        print(event.joy)
                        print(event.hat)
                        print(event.value)
        else :
            print("手柄连接失败")
    for i in range(joy_count):
        joy = joysticks[i]
        joy.quit()
else :
    print("手柄模块初始化失败")
joystick.quit()
pygame.quit()

