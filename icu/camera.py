import cv2

class Camera:
    # http://www.chioka.in/python-live-video-streaming-example/
    def __init__(self,ip):
        self.ip = ip
        if self.ip == '127.0.0.0':
            self.cam = cv2.VideoCapture(0)

    def __del__(self):
        if self.ip == '127.0.0.0':
            self.cam.release()

    def get_frame(self):
        sucess, image = self.cam.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def gen(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')