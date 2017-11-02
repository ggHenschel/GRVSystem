import json
import datetime
import cv2


class DetectMovement(object):

    def __init__(self):
        super().__init__()

        self.conf = json.load(open("conf.json"))
        self.avg = None
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0

    def process_image(self, frame):
        text = "Unoccupied"
        timestamp = datetime.datetime.now()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, tuple(self.conf['blur_size']), 0)

        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return [], False

        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        cv2.accumulateWeighted(gray, self.avg, 0.5)

        thresh = cv2.threshold(frameDelta, self.conf["delta_thresh"], 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        im2 ,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.conf["min_area"]:
                continue

            text = "Occupied"

            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


         # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)

        ###################################################################################
        # LOGIC
        ###################################################################################

        # check to see if the room is occupied
        if text == "Occupied":
                    # save occupied frame
                    cv2.imwrite("/tmp/talkingraspi_{}.jpg".format(self.motionCounter), frame);

                    # check to see if enough time has passed between uploads
                    if (timestamp - self.lastUploaded).seconds >= self.conf["min_upload_seconds"]:

                            # increment the motion counter
                            self.motionCounter += 1

                            # check to see if the number of frames with consistent motion is
                            # high enough
                            if self.motionCounter >= int(self.conf["min_motion_frames"]):
                                    # check to see if dropbox sohuld be used


                                    # update the last uploaded timestamp and reset the motion
                                    # counter
                                    self.lastUploaded = timestamp
                                    self.motionCounter = 0

        # otherwise, the room is not occupied
        else:
            self.motionCounter = 0

        if text == "Occupied":
            return frame, True

        return frame, False
