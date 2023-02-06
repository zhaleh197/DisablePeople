# from msilib import init_database
from ultralytics import YOLO
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

# create the app
# app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frinds.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SALALCHEMY_TRACK_MODIFICATIONS']=False
# initialize the app with the extension
# db.init_app(app) 


db = SQLAlchemy(app)
#Create Models
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(50))
    date_created=db.Column( db.DateTime,default=datetime.utcnow )

    #Create function to reuretn a string when  we add 
    def __repr__(self):
        # return '<Name %r>' %self.id
        return f'Friends({self.id}-{self.username}-{self.email}-{self.date_created})'


# @app.route(DETECTION_URL, methods=["POST"])
# def predict():
#     if not request.method == "POST":
#         return
#     if request.files.get("image"):
#         crop_base64=""
#         img_base64=""
#         crp_base64=""
#         imgm_base64=""
#         image_file = request.files["image"]
#         image_bytes = image_file.read()

#         img = Image.open(io.BytesIO(image_bytes))
#         now = datetime.now()
#         results = model(img, size=416)
#         data = results.pandas().xyxy[0].to_json(orient="records")
#         #  results = model(img, size=416)

#         # for debugging
#         data = results.pandas().xyxy[0]
#         print(data["name"])
#         if data["name"] is not None:
#             reschar=str(data["name"]).split("    ")[1]
#             reschar=reschar.split('\n')[0]
#             print(len(data))
#             scrp=[]
#             for index,item in data.iterrows():
#                 area= (int(item["xmin"])-5, int(item["ymin"])+5,int(item["xmax"])+10,int(item["ymax"])+5)
#                 # area = (0, 0, 68, 60)
#                 crop=img.crop(area)
#             #     crop = crop.resize((400,104))
#             #     ocrresults = ocrmodel(crop, size=320)
#             #     ocp=ocrresults.pandas().xyxy[0].sort_values(by=['xmin'])
#             #     # reschar=["".join(s) for s in ocp["name"].map(str)]
#             #     reschar=''.join([str(elem) for elem in ocp["name"]])
#             #     print(reschar)
#             #     if len(reschar)>5:
#             #         now = datetime.now()

#                 crop.save("static/image"+str(index)+str(reschar)+"_"+str(now).replace(":","_")+".jpg", format="JPEG")
#                 scrp.append({"image":str("static/image"+str(index)+str(reschar)+"_"+str(now).replace(":","_")+".jpg"),"label":reschar})
                
#                     # for crp in ocrresults.imgs:
#                     #     crop_base64 = Image.fromarray(crp)
#                     #     crp_base64=crp.tobytes()
#                     #     crop.save("static/crp"+str(reschar)+"_"+str(now).replace(":","_")+".jpg", format="JPEG")
#             for img in results.ims:
#                 img_base64 = Image.fromarray(img)
#                 imgm_base64=img.tobytes()
#                 img_base64.save("static/imageout_"+str(now).replace(":","_")+".jpg", format="JPEG")
#             print(img_base64)
        
#             res={
#                 "image":str("static/imageout_"+str(now).replace(":","_")+".jpg"),
#                 # "plate":str(base64.b64encode(crp_base64)),
#                 "character":str(reschar),
#                 "detect":scrp,
#                 "date":str(now)
#             }
#             return res
#         return ""

@app.route('/')
def home():
    # friends=Friends.query.all()
    model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    # Use the model
    results = model.train(data="coco128.yaml", epochs=3)  # train the model
    results = model.val()  # evaluate model performance on the validation set
    results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    success = model.export(format="onnx")  # export the model to ONNX format
    print("results", results)
    # friends="Hiiiiiiiiii shahla"
    return render_template('home.html', results=results)
    # return friends.username

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/<id>')
def detail(id):
    persn=Friends.query.get(id)
    return render_template('detail.html', persn=persn)
    
@app.route('/delete/<id>')
def delete(id):
    deletperson=Friends.query.get(id)
    db.session.delete(deletperson)
    db.session.commit()
    return redirect(url_for('home'))

# if __name__=='__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        # parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
        # parser.add_argument("--port", default=5000, type=int, help="port number")
        # args = parser.parse_args()

        # model = torch.hub.load('ultralytics/yolov5', 'custom', path='sdfbest.pt', force_reload=True) 
        # model.eval()
        # # ocrmodel = torch.hub.load('ultralytics/yolov5', 'custom', path='lastocrp.pt', force_reload=True) 
        # # ocrmodel.eval()
        # # app.run(host="192.168.1.2", port=2410)  # debug=True causes Restarting with stat
        
        
                # Load a model
        # model = YOLO("yolov8n.yaml")  # build a new model from scratch
        # model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

        # # Use the model
        # results = model.train(data="coco128.yaml", epochs=3)  # train the model
        # results = model.val()  # evaluate model performance on the validation set
        # results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
        # success = model.export(format="onnx")  # export the model to ONNX format
        # print("results", results)
        app.run(debug=True)

