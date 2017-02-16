import cv2
import subprocess, threading
import socket, time

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

# data = s.recv(512)
# print 'the data received is', data

video_capture = Grabber(cv2.VideoCapture("rtsp://10.157.20.76:5554/playlist.m3u"))
f = open("logs.txt", "r")
command = ""
while command != "end":
    command = raw_input()
    print ">>: ", command
    ret, frame = video_capture.retrieve()
    direction = command[:2]

    cv2.imwrite(direction + "/" + str(time.time()) +  ".jpg", frame)

    s.send(command+" 0.4")

s.close()
