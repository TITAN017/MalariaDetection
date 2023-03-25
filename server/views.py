from flask import Blueprint,request
from flask_mail import Message  
from . import detection_model as model
import cv2
import numpy as np
import json

img_type = ('Positive','Negative')
views = Blueprint('views',__name__)

def send_mail(header,addmsg,email = "madhacharya2@gmail.com"):
    from . import mail
    print('creating mail...')
    msg = Message(
                header,
                sender ='madhvesham.teamchimera@gmail.com',
                recipients = [email]
               )
    msg.body = addmsg
    mail.send(msg)
    print('mail sent successfully')
    
@views.route('/predict',methods = ['GET'])
def predict():
    npimg = cv2.imread('cell.png')
    #img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = cv2.resize(npimg,(224,224))
    #cv2.imwrite('cell.png',img)
    pred = img_type[model.predict(np.expand_dims(img,axis=0)).argmax()]
    pred = img_type[int(np.squeeze(np.round(model.predict(np.expand_dims(img,axis=0))),axis = (0,1)))]
    print(pred)
    #executor.submit(send_mail)
    return pred

@views.route('/custom_predict',methods = ['POST'])
def custom_predict():
    from . import executor
    file = request.json
    npimg = np.array(file['data']['data'],dtype=np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = cv2.resize(img,(224,224))
    cv2.imwrite('cell.png',img)
    pred = img_type[model.predict(np.expand_dims(img,axis=0)).argmax()]
    pred = img_type[int(np.squeeze(np.round(model.predict(np.expand_dims(img,axis=0))),axis = (0,1)))]
    print(pred)
    header = 'Alert: Report Generated!'
    addmsg = 'Report has been successfully generated, please head over to the website to view the report.'
    executor.submit(send_mail,header,addmsg)
    return json.dumps({'name':'Kaushik','success':pred})

@views.route('/adduser',methods = ['POST'])
def adduser():
    from . import executor
    file = request.json
    details = file
    print(details)
    header = "User Registered"
    addmsg = f"You have been successfully registered into the system\nUsername:{details['username']}\nPassword:{details['password']}"
    email = details['email']
    executor.submit(send_mail,header,addmsg,email)
    return file

@views.route('/test',methods = ['GET'])
def home():
    from . import executor
    header = 'testing'
    addmsg = 'just testing...'
    email = 'madhvesham.cs20@rvce.edu.in'
    executor.submit(send_mail,header,addmsg,email)
    return header + addmsg + email