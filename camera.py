from abc import ABCMeta, abstractmethod
import cv2
import time


class Camera(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._cap = None
        self._frame_count = 0
        self.set_time()

    def set_time(self):
        self._set_time = time.time()
    
    @property
    def spanTime(self):
        return time.time() - self._set_time

    def set_performance(self):
        self._frame_count = 0
        self.set_time()
    
    @property
    def frame_rate(self):
        return self._frame_count/self.spanTime

    @abstractmethod
    def open():
        pass
    
    @abstractmethod
    def isOpened():
        pass

    @abstractmethod
    def get_frame():
        '''get bytes with jpg format'''
        pass

    def gen(self):
        """Video streaming generator function."""
        while True:
            frame = self.get_frame()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    @property
    def frame_count(self):
        return self._frame_count

    

class LocalCamera(Camera):
    def __init__(self) -> None:
        super().__init__()

    def open(self):
        self._cap = cv2.VideoCapture(0)
        self._cap.set(3, 640)  # width=1920
        self._cap.set(4, 480)  # height=1080

    def isOpened(self):
        if self._cap == None:
            raise("null camera")
        else:
            return self._cap.isOpened()

    def get_frame(self):
        ret, frame = self._cap.read()

        img = frame
        img_encode = cv2.imencode('.jpg', img)[1]
        img_byte = img_encode.tobytes()
        self._frame_count += 1
        return img_byte
