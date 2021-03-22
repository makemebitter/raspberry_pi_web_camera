from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.http import Http404 
from multiprocessing import Manager, Process, Pool,Manager

import cv2
MANAGER = Manager()
CONTAINER = MANAGER.dict()
WRITER_PROC = None
VIDEO = None
SUCCESS = "SUCCESS"

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(-1)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def get_frame():
    success, image = VIDEO.read()
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()

def gen():
    while True:
        try:
            res = CONTAINER[0]
            yield res
        except Exception:
            raise Http404("Stream shut")


def gen_old(video_obj):
    while True:
        try:
            frame = video_obj.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception:
            raise Http404("Stream shut")





# Create your views here.


def video_feed(request):
    return StreamingHttpResponse(gen_old(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


def video_stop(request):
    global VIDEO
    global WRITER_PROC
    if VIDEO is None:
        raise Http404("Video already off")
    try:
        WRITER_PROC.terminate()
        VIDEO.release()
        VIDEO = None
        return HttpResponse("Camera turned off")
    except Exception:
        raise Http404("Failed to turn off camera")

def writer():
    success, image = VIDEO.read()
    # We are using Motion JPEG, but OpenCV defaults to capture raw images,
    # so we must encode it into JPEG in order to correctly display the
    # video stream.
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    content = (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    CONTAINER[0] = content



def video_start(request):
    global VIDEO
    global WRITER_PROC
    if VIDEO is not None:
        raise Http404("Video already on")
    else:
        try:
            VIDEO = cv2.VideoCapture(-1)
            p = Process(target=writer,args=()) # say to 'f', in which 'd' it should append
            p.start()
            WRITER_PROC = p
            return HttpResponse("Camera turned on")
        except Exception:
            raise Http404("Failed to turn off camera")



	