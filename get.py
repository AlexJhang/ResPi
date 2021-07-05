import requests
from requests.api import patch
import cv2
import numpy as np
import requests
# 使用 GET 方式下載普通網頁
#r = requests.get('http://192.168.1.100:8090/video_feed')


url = 'http://192.168.1.100:8090/video_feed'
res = requests.get(url, stream=True)  # steam=True不能少
bytes = b'\r\n'  # 目前收到的二进制内容
cst = b'\r\n--frame\r\nContent-Type: image/jpeg\r\n\r\n'
now = 0
next = -1
for chunk in res.iter_content(chunk_size=1024):
    bytes += chunk
    next = bytes.find(cst, now + 1)
    if -1 != next:  # 说明有新的一帧到了
        bin_data = bytes[now + len(cst):next]
        image = cv2.imdecode(np.frombuffer(bin_data, np.uint8),
                             cv2.IMREAD_UNCHANGED)
        cv2.imshow('frame', image)  # 只是为了显示
        cv2.waitKey(1)
        bytes = bytes[next:]
        now = 0
        next = -1
res.close()