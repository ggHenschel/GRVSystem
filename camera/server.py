#!/usr/bin/env python

import socket
import cv2
import pickle
import struct
import sys
#from detect_movement import DetectMovement
#from utils import send_email
import time
from camera.detect_movement import DetectMovement
from camera.utils import send_email
import json


def get_frame_from_camera():
    global data, payload_size
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
    return frame

  
def server_run():
    HOST = ''
    PORT = 8089
    FIVE_MINUTES = 5 * 60
    
    if len(sys.argv) < 2:
        print("[ERROR] No emails provided.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[INFO] Socket created')

    s.bind((HOST, PORT))
    print('[INFO] Socket bind complete')

    s.listen(10)
    print('[INFO] Socket now listening')



    global data, payload_size, conn, addr
    conn, addr = s.accept()
    data = bytearray()
    payload_size = struct.calcsize("L")
    detect = DetectMovement()
    
    timeLastEmailSent = 0


    while True:
        frame = get_frame_from_camera()
        frame, movement = detect.detect(frame)

        if movement:
            # Epoch atual
            cur_min = time.time()

            # Verifica se passou 5 minutos do ultimo alerta
            if timeLastEmailSent + FIVE_MINUTES < cur_min:
                print("[INFO] Time of breach: " + time.ctime())
                timeLastEmailSent = cur_min
                send_email()

        # Remover quando mandar a imagem pro servidor
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
