from PyQt5.QtCore import QThread,Qt,pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import time
from simple_facerec import SimpleFacerec
import csv

class Detection(QThread):
    x1=y1=''
    def __init__(self,x,y):
        super(Detection,self).__init__()
        self.x1=x
        self.y1=y

    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.running=True

        net = cv2.dnn.readNet("weights/yolov3_custom.weights","cfg/yolov3_custom.cfg")
        classes=[]

        with open("obj.names","r")as f:
            classes=[line.strip() for line in f.readlines()]
        
        layer_names = net.getLayerNames()
        output_layers=[layer_names[i-1] for i in net.getUnconnectedOutLayers()]
        # output_layers=net.getUnconnectedOutLayersNames()

        color = np.random.uniform(0,255,size=(len(classes),3))

        font=cv2.FONT_HERSHEY_PLAIN
        starting_time = time.time()

        #fce
        from datetime import datetime

        sfr = SimpleFacerec() #fce
        sfr.load_encoding_images("images/") 

        datetime=datetime.now()
        datef=datetime.strftime("%Y/%m/%d")
        timef=datetime.strftime("%H-%M-%S")
        #fce


        cap=cv2.VideoCapture(0)

        while self.running:
            ret,frame=cap.read()

            

            if ret:
                height,width,channels=frame.shape

                blob=cv2.dnn.blobFromImage(frame,0.00392,(416,416),(0,0,0),True,crop=False)
                net.setInput(blob)
                outs=net.forward(output_layers)

                class_ids=[]
                confidences=[]
                boxes=[]
                for out in outs:
                    for detection in out:
                        scores=detection[5:]
                        class_id = np.argmax(scores)
                        confidence=scores[class_id]

                        if confidence>0.50:
                            center_x=int(detection[0]*width)
                            center_y=int(detection[1]*height)
                            w=int(detection[2]*width)
                            h=int(detection[3]*height)

                            x=int(center_x-w/2)
                            y=int(center_y-h/2)

                            boxes.append([x,y,w,h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                
                indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)

                for i in range(len(boxes)):
                    if i in indexes:
                        global weapon
                        x,y,w,h=boxes[i]
                        weapon = label=str(classes[class_ids[i]])
                        confidence=confidences[i]
                        color=(256,0,0)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                        cv2.putText(frame,label+"{0:.1%}".format(confidence),(x,y-20),font,3,color,3)

                        elapsed_time=starting_time-time.time()

                        if elapsed_time<=-10:
                            starting_time=time.time()
                            self.save_detection(frame)


                #fce
                face_locations, face_names = sfr.detect_known_faces(frame)
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                    # cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 0), 4)
                    if(name=="Unknown"):
                        
                        continue
                    else:
                        with open('face_csv/Faces_detected.csv','a',newline='') as f:
                            lnwriter=csv.writer(f)
                            lnwriter.writerow([name,datef,timef])
                            #fce

                rgbImage=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                bytesPerLine = channels*width
                convertToQtFormat=QImage(rgbImage.data,width,height,bytesPerLine,QImage.Format_RGB888)
                p=convertToQtFormat.scaled(854,480,Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            
    def save_detection(self,frame):
        
        import mysql.connector
        from datetime import datetime
        import json
        from urllib.request import urlopen
        from twilio.rest import Client



        url='https://ipinfo.io/json'
        res=urlopen(url)

        mysql=mysql.connector.connect(
            host="localhost",
            user="jithin",
            passwd="jithin",
            database="crime_detect"
        )
        datetime=datetime.now()
        date=datetime.strftime("%Y/%m/%d")
        time=datetime.strftime("%H:%M:%S")
        mycursor=mysql.cursor()

        sendto='+91'+self.x1
        loc=json.load(res)
        loc=self.y1
        sql="insert into detect(DATE,TIME,LOCATION,WEAPON,SENT_TO,IMAGE) values(%s,%s,%s,%s,%s,%s)"

        with open('saved_frame/frame.jpg','rb')as fr:
            frame_bytes=fr.read()
        cv2.imwrite("saved_frame/frame.jpg",frame)

        sid='AC49af97cd8e4a643400ff119e69fd6080'
        auth='3a903437c91ac2cd627bed926b6eab85'
        client=Client(sid,auth)
        msg='A '+str(weapon)+' was detected at '+loc+' today('+date+') '+time+'.'
        client.messages.create(
            body=msg,
            from_='+12525074002',
            to=sendto,
        )

        val=[date,time,loc,str(weapon),sendto,frame_bytes]
        mycursor.execute(sql,val)
        print("Frame Saved")
        mysql.commit()