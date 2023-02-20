


from datetime import datetime
import threading
import time

import cv2
from EasyROI import EasyROI
import json
import cv2
from pprint import pprint
from ultralytics import YOLO
from PIL import Image
import cv2
from shapely.geometry import Polygon
from shapely.geometry import box as bbox
import numpy
from EasyROI import EasyROI
import requests
import base64
roi_helper = EasyROI(verbose=True)
url = 'http://127.0.0.1:8000/detect'
import asyncio

def intersect(poly, rect):
    perst = dict()
    for index, roi in poly['roi'].items():
        poly_vertices = roi['vertices']

    # Create a polygon
        polygon = Polygon(poly_vertices)

        # Create a rectangle
        rectangle = bbox(rect[0], rect[1], rect[2], rect[3])

        # Get the intersection
        intersection = polygon.intersection(rectangle)

        # Print the intersection area
        percentage = intersection.area / rectangle.area * 100
        perst[index] = percentage

        # print(percentage)
    return perst

# load a pretrained model (recommended for training)
# model1 = YOLO("yolov8n.pt")
# model = YOLO("bestDisable.pt")
# model=YOLO('bestnew.pt')

model1=YOLO('./runs/detect/train/weights/bestnew.pt')
colorobj=(0,255,0)
colorroiStart=(255,0,0)
colorroiPath=(255,255,255)


# polygon_roiStart = dict()
# with open('res.json') as f:
#     data = json.loads(f.read().replace("\'", "\""))
# print(type(data))
# for item in data:
#     vl = [x for x in data[item]['vertices'][1:-1].split(' ,  ')]
#     fl = []
#     for xl in vl:
#         fl.extend(eval(xl))
#     data[item]['vertices'] = fl
# polygon_roiStart['roi'] = data

# polygon_roiStart['type'] = 'polygon'


# polygon_roiPath = dict()
# with open('res.json') as f:
#     data = json.loads(f.read().replace("\'", "\""))
# print(type(data))
# for item in data:
#     vl = [x for x in data[item]['vertices'][1:-1].split(' ,  ')]
#     fl = []
#     for xl in vl:
#         fl.extend(eval(xl))
#     data[item]['vertices'] = fl
# polygon_roiPath['roi'] = data

# polygon_roiPath['type'] = 'polygon'



class Camera:
    def __init__(self):
        self.thread = None
        self.current_frame = None
        self.last_access = None
        self.res = None
        self.is_running: bool = False
        self.camera = cv2.VideoCapture("1.mp4")
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # load a pretrained model (recommended for training)
        # self.model = YOLO("yolov8n.pt")

    def __del__(self):
        self.camera.release()
   
    def start(self):#def start(self,counter):

        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()
            
            # counter+=1
            # self.thread.start() 
            # if counter%5==0:
                # self.thread = threading.Thread(target=self._capture)
                # self.thread.start()
            # counter+=1
            # self.thread.start()    
    def get_frame(self):
        self.last_access = time.time()

        return self.current_frame, self.res

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None
    
    def _capture(self):
        # counter=0
        self.is_running = True
        self.last_access = time.time()
        time.sleep(1)
        
         # Initialize cam
        cap=self.camera
        ret, frame = cap.read()
        # roi_helper = EasyROI(verbose=True) 
        polygon_roiStart = roi_helper.draw_polygon(frame, 1) 
        # print("Polygon start:")
        # pprint(polygon_roiStart)
        frame = roi_helper.visualize_roi(frame, polygon_roiStart)
        polygon_roiPath = roi_helper.draw_polygon(frame, 1) 

        # print("Polygon Path:")
        # pprint(polygon_roiPath)
        # ######important Parameters
        CounterFrametoRed_start=0
        CounterFrametoGreen_end=0
        Light=0 #=="Green"
    # ########3
        while self.is_running:
        # while True:
            ret, frame = self.camera.read()
        #  if 5%5==0:
            #* ret, frame = self.camera.read()

            # results = model1.predict(frame , conf=0.01 )
            # results=model1.predict(frame, confidence=0.1, overlap=0.1) 
            results = model1.predict(source=frame, conf=0.1)
            
            keys = []
            mdata = dict()
            # results = results.numpy()
            # img2 = YOLO..visualize(frame, results)
            # cv2.imshow(img2)
            # cv2.waitKey(1)

            ########### Frame Process
            colorroi = (255, 0, 0)
            for result in results:
                boxes = result.boxes
                if (len(boxes)==0 & Light==1):
                    CounterFrametoGreen_end+=1
                    if(CounterFrametoGreen_end>=10):#==7 ثانیه    
                        Light=0 #Green
                        CounterFrametoGreen_end=0
                elif len(boxes)>0:
                    for box in boxes:
                        keys = []
                        # if box.cls[0] == float(0):
                        for bxy in box.xyxy:
                            if Light==0:
                                tx=numpy.array(bxy)
                                insect=intersect(polygon_roiStart,[int(tx[0]), int(tx[1]), int(tx[2]), int(tx[3])])
                                v1 = {
                                    k1: v1 for (k1, v1) in insect.items() if v1 > 20}
                                if len(v1) > 0:
                                    CounterFrametoRed_start+=1
                                    colorobj=(10,50,352)
                                    colorroi=(0,50,245)
                                    if(CounterFrametoRed_start>=1):#==3 ثانیه    #for test thi is 1 fram. by for real this must be 30 . 
                                        Light=1 #Red
                                        CounterFrametoRed_start=0
                                #################################  save frame  
                                    # print(keys)
                                    # cv2.waitKey(1)
                                    
                                    cv2.rectangle(frame, (int(tx[0]), int(
                                        tx[1])), (int(tx[2]), int(tx[3])), colorobj, 1)
                                   
                                    _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
                                    base64_img = base64.b64encode(encoded_img).decode("utf-8")
                                    mdata = {
                                     "classobj": int(box.cls[0]),
                                     "boundry": str(tx).replace("       ",","),
                                        # "imgcroped": "base64_crop",
                                        # "xyxy": str(tx).replace("       ",","),
                                    "lightflag":Light,
                                     "date_created": str(datetime.now().strftime('%H:%M:%S')),
                                     "img":base64_img,
                                     "date2":str(datetime.today().strftime('%Y-%m-%d')),
                                    }
                                    headers = {"Accept": "application/json",
                                               "Content-Type": "application/json; charset=utf8"}
                                    data = json.dumps(mdata)
                                    try:
                                        # call get service with headers and params
                                        response = requests.post(
                                            url, data=data, headers=headers)
                                        print(response)
                                    except Exception as ex:
                                        print(ex)    
                                # print(tx[0])
                                    #################################save frame  
                                            
                            elif Light==1:
                                tx = numpy.array(bxy)
                                insect = intersect(
                                    polygon_roiPath, [int(tx[0]), int(tx[1]), int(tx[2]), int(tx[3])])
                                v = {
                                    k: v for (k, v) in insect.items() if v > 20}
                                insect = intersect(
                                    polygon_roiStart, [int(tx[0]), int(tx[1]), int(tx[2]), int(tx[3])])
                                vstart = {
                                    kstart: vstart for (kstart, vstart) in insect.items() if vstart > 20}
                                if len(v) > 0 or len(vstart) > 0:
                                    colorobj = (0, 0, 255)
                                    # k = list(v.keys())
                                    # keys.extend(k)
                                    # print(keys)
                                    
                                    # cv2.waitKey(1)
                                    cv2.rectangle(frame, (int(tx[0]), int(
                                        tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)
                                    
                                   
                                    _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
                                    base64_img = base64.b64encode(encoded_img).decode("utf-8")
                                    mdata = {
                                     "classobj": int(box.cls[0]),
                                     "boundry": str(tx).replace("       ",","),
                                        # "imgcroped": "base64_crop",
                                        # "xyxy": str(tx).replace("       ",","),
                                    "lightflag":Light,
                                     "date_created": str(datetime.now().strftime('%H:%M:%S')),
                                     "img":base64_img,
                                     "date2":str(datetime.today().strftime('%Y-%m-%d')),
                                    }
                                    headers = {"Accept": "application/json",
                                               "Content-Type": "application/json; charset=utf8"}
                                    data = json.dumps(mdata)
                                    try:
                                        # call get service with headers and params
                                        response = requests.post(
                                            url, data=data, headers=headers)
                                        print(response)
                                    except Exception as ex:
                                        print(ex)

                                else:
                                    # tx=numpy.array(bxy)
                                    # colorobj = (0, 255, 0)
                                    # cv2.rectangle(frame, (int(tx[0]), int(tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)
                                    CounterFrametoGreen_end+=1
                                    colorobj=(10,0,255)
                                    colorroi=(0,10,245)
                                    
                                    if(CounterFrametoGreen_end>=3):#==7 ثانیه    #for test thi is 10 fram. by for real this must be 100
                                        Light=0 #Green
                                        CounterFrametoGreen_end=0
                                    #################################    save frame  
                                    # print(keys)
                                    # cv2.rectangle(frame, (int(tx[0]), int(
                                    #     tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)
                                   
                                    _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
                                    base64_img = base64.b64encode(encoded_img).decode("utf-8")
                                    mdata = {
                                     "classobj": int(box.cls[0]),
                                     "boundry": str(tx).replace("       ",","),
                                        # "imgcroped": "base64_crop",
                                        # "xyxy": str(tx).replace("       ",","),
                                    "lightflag":Light,
                                     "date_created": str(datetime.now().strftime('%H:%M:%S')),
                                     "img":base64_img,
                                     "date2":str(datetime.today().strftime('%Y-%m-%d')),
                                    }
                                    headers = {"Accept": "application/json",
                                               "Content-Type": "application/json; charset=utf8"}
                                    data = json.dumps(mdata)
                                    try:
                                        # call get service with headers and params
                                        response = requests.post(
                                            url, data=data, headers=headers)
                                        print(response)
                                    except Exception as ex:
                                        print(ex)    
                                # print(tx[0])
                                    #################################   
                       
                    #################################    

                        
                    # frame = roi_helper.visualize_roi(
                    # frame, polygon_roiStart)
                    # frame = roi_helper.visualize_roi(
                    # frame, polygon_roiPath)
                    # cv2.imshow("frame zhhhhh", frame)
                    # key = cv2.waitKey(1)
                    # print(box.xyxy )

                        # _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
                        # base64_img = base64.b64encode(encoded_img).decode("utf-8")
                        # mdata = {
                        # "classobj": int(box.cls[0]),
                        # "boundry": str(tx).replace("       ",","),
                        # "lightflag":Light,
                        #  "date_created": str(datetime.datetime.now().strftime('%H:%M:%S')),
                        #  "img":base64_img,
                        #  }
                        # headers = {"Accept": "application/json",
                        #   "Content-Type": "application/json; charset=utf8"}
                        # data = json.dumps(mdata)
                        # try:
                        #                 # call get service with headers and params
                        #     response = requests.post(url, data=data, headers=headers)
                        #     print(response)
                        # except Exception as ex:
                        #     print(ex) 
                frame = roi_helper.visualize_roi(
                    frame, polygon_roiStart)
                frame = roi_helper.visualize_roi(
                    frame, polygon_roiPath)
                cv2.imshow("frame zhhhhh", frame)
                key = cv2.waitKey(1)
                self.res = mdata
            


            #####################
            # frame = roi_helper.visualize_roi(
            #         frame, polygon_roiStart)
            # frame = roi_helper.visualize_roi(
            #         frame, polygon_roiPath)
            # cv2.imshow("frame",frame)
            # cv2.waitKey(1)

            #####
         
            if ret:
                    ret, encoded = cv2.imencode(".jpg", frame)
                    if ret:
                        self.current_frame = encoded
                    else:
                        print("Failed to encode frame")
            else:
                    print("Failed to capture frame")

                ##new with counter to faster     
            print("Reading thread stopped")
        #  counter+=1
        #  self.thread = None
        #  self.is_running = False

            # print("Reading thread stopped")
       
        self.thread = None
        self.is_running = False
        
        # return True


