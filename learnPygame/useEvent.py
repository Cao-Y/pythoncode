#handle the key event
import pygame
from pygame.locals import *
from sys import exit
'''
    事件                         产生途径                            参数
    QUIT                 用户按下关闭按钮                    none
    ATIVEEVENT                 Pygame被激活或者隐藏                    gain, state
    KEYDOWN                 键盘被按下                            unicode, key, mod
    KEYUP                 键盘被放开                            key, mod
    MOUSEMOTION                 鼠标移动                            pos, rel, buttons
    MOUSEBUTTONDOWN         鼠标按下                            pos, button
    MOUSEBUTTONUP         鼠标放开                            pos, button
    JOYAXISMOTION         游戏手柄(Joystick or pad)移动           joy, axis, value
    JOYBALLMOTION         游戏球(Joy ball)?移动            joy, axis, value
    JOYHATMOTION         游戏手柄(Joystick)?移动            joy, axis, value
    JOYBUTTONDOWN         游戏手柄按下                            joy, button
    JOYBUTTONUP                 游戏手柄放开                            joy, button
    VIDEORESIZE                 Pygame窗口缩放                    size, w, h
    VIDEOEXPOSE                 Pygame窗口部分公开(expose)            none
    USEREVENT                 触发了一个用户事件                    code
'''
__author__ = {'name' : 'Hongten',
              'mail' : 'hongtenzone@foxmail.com',
              'QQ'   : '648719819',
              'Version' : '1.0'}
BG_IMAGE = '../learnCv/1.png'
pygame.init()
pygame.joystick.init()
joy = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for i in range(pygame.joystick.get_count()):
    joy[i].init()
screen = pygame.display.set_mode((500, 500), 0, 32)
bg = pygame.image.load(BG_IMAGE).convert()
x, y = 0, 0
move_x, move_y = 0, 0
while 1:
    for event in pygame.event.get():
        #print(event.type)
        if event.type == QUIT:
            exit()
        if event.type == JOYBUTTONDOWN:
            print(event)
            #event.key返回的是一个数字值，而K_LEFT,K_UP,K_RIGHT,K_DOWN等都是常量，
            #他们代表的也是一个数字值，这些数字值可以用：print(event.key)获取到
            #如：K_LEFT = 276
            #   K_UP = 273
            #所以下面的代码可以替换为：
            #if event.key == 276:
            #    move_x = -10
            # if event.key == K_LEFT:
            #     move_x = -10
            # elif event.key == K_UP:
            #     move_y = -10
            # elif event.key == K_RIGHT:
            #     move_x = 10
            # elif event.key == K_DOWN:
            #     move_y = 10
        elif event.type == KEYUP:
            move_x = 0
            move_y = 0
        x += move_x
        y += move_y
        #print(x, y)
        screen.fill((0, 0, 0))
        screen.blit(bg, (x, y))
        pygame.display.update()
