# from EasyROI import EasyROI
from tkinter import PhotoImage
from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import argparse
import io
from PIL import Image
from datetime import datetime
import torch
from flask import Flask, request
import base64 
from pprint import pprint
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy 
# from flask_appbuilder.models.mixins import ImageColumn

app = Flask(__name__)
from flask_cors import CORS

DETECTION_URL = "/api/upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///objectdetection.db'
db = SQLAlchemy(app)
 

class MyPanel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    classobj=db.Column(db.Integer)
    boundry=db.Column(db.String(60))
    date_created=db.Column( db.DateTime,default=datetime.now) 
    img = db.Column(db.String(1000))
    # img = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))

    #Create function to reuretn a string when  we add 
    def __repr__(self):
        return f'MyPanel({self.id}-{self.classobj}-{self.date_created})'  
        
# model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
model1=YOLO('./runs/detect/train/weights/best.pt')
colorobj=(0,255,0)
colorroi=(255,0,0)


@app.route('/')
def home():
    # # friends=Friends.query.all()
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    # model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    # # Use the model
    # results = model.train(data="coco128.yaml", epochs=3)  # train the model
    # results = model.val()  # evaluate model performance on the validation set
    # results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    # success = model.export(format="onnx")  # export the model to ONNX format


    
    # model1=YOLO('./runs/detect/train/weights/best.pt')
    # # model.predict( source='0' ,save=True, conf=0.2, save_txt=True)
    # results=model1.predict( source='1.jpg' ,save=True, conf=0.2, save_txt=True)




    video_path ="a.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter('output.avi',fourcc,  20.0, (1280,720))
    # Initialize cam
    cap = cv2.VideoCapture("b.mp4")
    while True:
        ret, frame = cap.read()
        # DRAW POLYGON ROI
        results = model1.predict(frame)
        for result in results:
            data=[]
            colorroi=(255,0,0)
            boxes=result.boxes
            if len(boxes)>0:
                for box in boxes:
                    if box.cls[0]==float(0):
                        for bxy in box.xyxy:
                            tx=numpy.array(bxy)
                            crop=frame[ int(tx[1]):  int(tx[3]), int(tx[0]) :int(tx[2])]
                            cv2.imshow("crop", crop)
                            img_base64 = Image.fromarray(crop)
                            imgm_base64=crop.tobytes()
                            res={"class":int(box.cls[0]),
                                "boundry":tx,
                                "img":imgm_base64
                                }
                            print('imgm_base64 ***************************:   ',imgm_base64)
                            print('\n')
                            print('\n')
                            print('img  ................................ ',img_base64)
                            op=MyPanel(
                            classobj=res["class"],
                            boundry=str(res["boundry"]),
                            img=res["img"]
                            )
                            db.session.add(op)
                            db.session.commit()

                            render_template('showobject.html',results=op)

                            cv2.waitKey(1)
                            cv2.rectangle(frame, (int(tx[0]), int(tx[1])), (int(tx[2]), int(tx[3])),colorobj, 2)

                
                # print(box.xyxy )


        # frame_temp = roi_helper.visualize_roi(frame, polygon_roi)
        # writer.write(frame_temp)
        # pprint(polygon_roi)
    #  
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        # if key & 0xFF == ord('q'):
        #     writer.release()
        #     cv2.destroyAllWindows()


        # # '''
        # cv2.imshow("frame", frame)
        # key = cv2.waitKey(0)
        # if key & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        # # '''


    results="jkjhk"    
    print("results", results) 
    return render_template('home.html', results=results)

@app.route('/About/')
def about():
    results="Hiiiiiiiiii shahla"
    return render_template('About.html', results=results)

@app.route('/get/<object_id>')
def detailpost(object_id):
    results=MyPanel.query.get_or_404(object_id)
    return render_template('showobject.html',results=results)

if __name__=='__main__':
  with app.app_context():
    app.run(debug=True)

    # video_path ="a.mp4"
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # writer = cv2.VideoWriter('output.avi',fourcc,  20.0, (1280,720))
    # # Initialize cam
    # cap = cv2.VideoCapture("b.mp4")
    # while True:
    #     ret, frame = cap.read()
    #     # DRAW POLYGON ROI
    #     results = model.predict(frame)
    #     for result in results:
    #         data=[]
    #         colorroi=(255,0,0)
    #         boxes=result.boxes
    #         if len(boxes)>0:
    #             for box in boxes:
    #                 if box.cls[0]==float(0):
    #                     for bxy in box.xyxy:
    #                         tx=numpy.array(bxy)
    #                         crop=frame[ int(tx[1]):  int(tx[3]), int(tx[0]) :int(tx[2])]
    #                         cv2.imshow("crop", crop)
    #                         img_base64 = Image.fromarray(crop)
    #                         imgm_base64=crop.tobytes()
    #                         res={"class":int(box.cls[0]),
    #                             "boundry":tx,
    #                             "img":imgm_base64
    #                             }
    #                         print('imgm_base64 ***************************:   ',imgm_base64)
    #                         print('\n')
    #                         print('\n')
    #                         print('img  ................................ ',img_base64)
    #                         op=MyPanel(
    #                         classobj=res["class"],
    #                         boundry=str(res["boundry"]),
    #                         img=res["img"]
    #                         )
    #                         db.session.add(op)
    #                         db.session.commit()
    #                         render_template('showobject.html',results=op)
    #                         cv2.waitKey(1)
    #                         cv2.rectangle(frame, (int(tx[0]), int(tx[1])), (int(tx[2]), int(tx[3])),colorobj, 2)

                
    #             # print(box.xyxy )


    #     # frame_temp = roi_helper.visualize_roi(frame, polygon_roi)
    #     # writer.write(frame_temp)
    #     # pprint(polygon_roi)
    # #  
    #     cv2.imshow("frame", frame)
    #     key = cv2.waitKey(1)
    #     # if key & 0xFF == ord('q'):
    #     #     writer.release()
    #     #     cv2.destroyAllWindows()


    #     # # '''
    #     # cv2.imshow("frame", frame)
    #     # key = cv2.waitKey(0)
    #     # if key & 0xFF == ord('q'):
    #     #     cv2.destroyAllWindows()
    #     # # '''



   