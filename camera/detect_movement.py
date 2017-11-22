import json
import datetime
import cv2

OCCUPIED = "Occupied"
UNOCCUPIED = "Unoccupied"


class DetectMovement(object):

    def __init__(self):
        super().__init__()

        self.conf = json.load(open("conf.json"))
        self.avg = None
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0

    def detect(self, frame):
        self.status = UNOCCUPIED
        self.timestamp = datetime.datetime.now()
        self.frame = frame

        self._detect_movement()

        if self.cnts is None:
            return self.frame, False

        self._add_detected_areas()

        self._update_text()

        if self.status == OCCUPIED:
            self._update_frame()

        else:
            self.motionCounter = 0

        if self.status == OCCUPIED:
            return frame, True

        return frame, False

    def _update_frame(self):
        # save occupied frame
        cv2.imwrite("/tmp/talkingraspi_{}.jpg".format(self.motionCounter), self.frame);

        # check to see if enough time has passed between uploads
        if (self.timestamp - self.lastUploaded).seconds >= self.conf["min_upload_seconds"]:

                # increment the motion counter
                self.motionCounter += 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if self.motionCounter >= int(self.conf["min_motion_frames"]):
                        self.lastUploaded = self.timestamp
                        self.motionCounter = 0

    def _add_detected_areas(self):
        # loop over the contours
        for c in self.cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.conf["min_area"]:
                continue

            self.status = OCCUPIED

            self._update_text()

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def _detect_movement(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, tuple(self.conf['blur_size']), 0)

        if self.avg is None:
            self.avg = gray.copy().astype("float")
            self.cnts = None
            return

        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        cv2.accumulateWeighted(gray, self.avg, 0.5)

        thresh = cv2.threshold(frameDelta, self.conf["delta_thresh"], 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        im2, self.cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

    def _update_text(self):
        # draw the text and timestamp on the
        ts = self.timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(self.frame, "Room Status: {}".format(self.status), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(self.frame, ts, (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
