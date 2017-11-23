#!/usr/bin/env python

import socket
import pickle
import struct
from camera.camera_feed import VideoCamera

def camera():
    HOST = 'localhost'
    PORT = 8089

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    camera = VideoCamera()

    while True:
        frame = camera.get_frame()
        data = pickle.dumps(frame)

        client.sendall((struct.pack("L", len(data)) + data))
