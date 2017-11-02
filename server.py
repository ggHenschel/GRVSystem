#!/usr/bin/env python

import socket
import cv2
import pickle
import struct
from detect_movement import DetectMovement

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

    frame, movement = detect.process_image(frame)

    # Remover quando mandar a imagem pro servidor
    if frame != []:
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
