import pygame.camera
import time
import pygame
import cv2
import numpy as np


def surface_to_string(surface):
    """convert pygame surface into string"""
    return pygame.image.tostring(surface, 'RGB')


def pygame_to_cvimage(surface):
    """conver pygame surface into  cvimage"""

    # cv_image = np.zeros(surface.get_size, np.uint8, 3)
    image_string = surface_to_string(surface)
    image_np = np.fromstring(image_string, np.uint8).reshape(480, 640, 3)
    frame = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    return image_np, frame


pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", [640, 480])

cam.start()
time.sleep(0.1)
screen = pygame.display.set_mode([640, 480])

while True:
    image = cam.get_image()

    cv_image, frame = pygame_to_cvimage(image)

    screen.fill([0, 0, 0])
    screen.blit(image, (0, 0))
    pygame.display.update()
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    # pygame.image.save(image, "pygame1.jpg")

cam.stop()



