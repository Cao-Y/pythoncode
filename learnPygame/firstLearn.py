# -*- coding: utf-8 -*-
from pygame import joystick

joystick.init()
print(joystick.Joystick(0))
joy = joystick.Joystick(0)
joy.init()
name =joy.get_name()
print(name)
#joysticks = joystick.joustick[0]

