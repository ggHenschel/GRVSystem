#!/usr/bin/env python

import socket
import cv2
import pickle
import struct
from camera.detect_movement import DetectMovement
from camera.utils import send_email
import json

def server_run():
    HOST = ''
    PORT = 8089

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[INFO] Socket created')

    s.bind((HOST, PORT))
    print('[INFO] Socket bind complete')

    s.listen(10)
    print('[INFO] Socket now listening')

    conn, addr = s.accept()

    data = bytearray()
    payload_size = struct.calcsize("L")

    detect = DetectMovement()

    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)

        frame, movement = detect.detect(frame)

        if movement:
            try:
                open("mail.lock", "r")
            except IOError:
                open("mail.lock", "w+")
                js = open("camera/conf.json")
                conf = json.load(js)
                send_email(conf)

        # Remover quando mandar a imagem pro servidor
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
