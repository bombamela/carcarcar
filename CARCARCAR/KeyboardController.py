import socket, time
import subprocess, threading
import pygame
from pygame.locals import *
import cv2
import numpy


class Grabber(threading.Thread):
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam = cam
        self.lock = threading.Lock()
        self.running = True
        self.start()
    def run(self):
        while self.running:
            time.sleep(0.01)
            with self.lock:
                self.cam.grab()
    def stop(self):
        self.running = False
    def retrieve(self):
        with self.lock:
            return self.cam.retrieve()
    def restart(self):
        self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)


address = ('10.157.120.47', 8009)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)


camera = Grabber(cv2.VideoCapture("rtsp://10.157.20.76:5554/playlist.m3u"))


#This shows an image weirdly...
screen_width, screen_height = 640, 480
screen=pygame.display.set_mode((screen_width,screen_height))

def getCamFrame(camera):
    retval,frame=camera.retrieve()
    framepygame=numpy.rot90(frame)
    framepygame=cv2.flip(framepygame, 0)
    framepygame=cv2.cvtColor(framepygame,cv2.COLOR_BGR2RGB)
    framepygame=pygame.surfarray.make_surface(framepygame) #I think the color error lies in this line?
    return framepygame, frame

def blitCamFrame(frame,screen):
    screen.blit(frame,(0,0))
    return screen

screen.fill(0) #set pygame screen to black

running=True
while running:
    framepygame, frame=getCamFrame(camera)
    screen=blitCamFrame(framepygame,screen)
    pygame.display.flip()
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                cv2.imwrite( "ll/" + str(time.time()) +  ".jpg", frame)
                s.send("ll 0.4")
            if event.key == K_RIGHT:
                cv2.imwrite( "rr/" + str(time.time()) +  ".jpg", frame)
                s.send("rr 0.4")
            if event.key == K_UP:
                cv2.imwrite( "ff/" + str(time.time()) +  ".jpg", frame)
                s.send("ff 0.4")
            if event.key == K_DOWN:
                cv2.imwrite( "bb/" + str(time.time()) +  ".jpg", frame)
                s.send("bb 0.4")
            if event.key == K_e:
                running = False

pygame.quit()
cv2.destroyAllWindows()
