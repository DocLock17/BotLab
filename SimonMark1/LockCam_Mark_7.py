#!/usr/bin/env python3

import io
import os
import sys
import time
import glob
import shutil
import picamera
import logging
import webbrowser 
import numpy as np
import smtplib, ssl
from numpy import asarray
import socketserver
from time import sleep
from threading import Condition
from http import server
from PIL import Image
from urllib.parse import parse_qs


notificationType = 0
captureStillOn = True

notDelay = 300 # 5 Minute
#notDelay = 900 # 15 Minute
#notDelay  = 3600 # 1 Hour
ownerEmail = "notify.lockindustries@gmail.com" #"michael.c.locker@gmail.com"
notificationAuth = "NotifyMe1!"

captureRate = 30 # yields one every Second (because it matches the framerate)
#captureRate = 300 # yields one every 10 Seconds
#captureRate = 1800 # yields one every Minute
#captureRate = 108000 # yields one every Hour
#captureRate = 2592000 # yields one every Day

shutdownFlag = 'R'
PAGE=str(open("index.html", "r").read())
styleSheet=str(open("style.css", "r").read())
# i need to put some kind of wait command here to allow the page to fully load

count = 0
global imgNum
imgNum = 0
notTimerSet = time.perf_counter()
inferIdentity=False

def turingCheck(sample):
    # Provides space for human check
    sizedSampleArray = np.array(Image.open(io.BytesIO(sample)).resize((224,224),))
    result = False
    return result

def indentityCheck(sample):
    # Provides space for indetity check
    result = False
    return result

def engageBolt():
    # Provides space for engaging lock
    callback = True
    return callback

def disengageBolt():
    # Provides space for disengaging lock
    callback = True
    return callback

def logVisitor():
    return    

def extractFiles(folderPath, folderName, subFolder=''):
    
    # Setup path variables
    copyName = folderName+'_Extractable_'+(time.strftime("%m%d%y_%H%M%S", time.gmtime()))
    copyPath = folderPath+copyName
    zipPath = folderPath+subFolder+copyName
    transferredFiles = glob.glob(folderPath+folderName+'/*')
    
    # Copy files from src to destination
    shutil.copytree(folderName, copyPath)
    
    # Zip temporary files into target location
    try:
        shutil.make_archive(zipPath, 'zip', folderPath, copyName)
    except OSError:
        pass
    
    # Clean up transferred Images
    for f in transferredFiles:
        os.remove(f)
        
    # Clean up tempory file
    shutil.rmtree(copyPath)
    
    return

def sequenceCapture():
    global count
    global imgNum
    global referenceImg
    global testImg1
    global testImg2
    global notTimerSet
    extractionThreshold = 500 #00
    frame = output.frame
    count += 1
    visitorID = ''
    
    if count%captureRate==0:
        if count==captureRate:
            referenceImg = np.array(Image.open(io.BytesIO(frame)))
            testImg1 = np.array(Image.open(io.BytesIO(frame)))
        else:
            testImg2 = np.array(Image.open(io.BytesIO(frame)))
            imgMSE1 = int(mse(referenceImg, testImg1))
            imgMSE2 = int(mse(referenceImg, testImg2))
            imgMSE3 = int(mse(testImg1, testImg2))
            referenceImg = testImg1
            testImg1 = testImg2
            if (imgMSE1>=1000) or (imgMSE2>=1000) or (imgMSE3>=1000):   
                if captureStillOn==True:
                    if imgNum>=extractionThreshold:
                        extractFiles('/home/pi/CameraProject/','sampleImages','extraction/')
                        imgNum = 0
                    with open("sampleImages/img" + time.strftime("%m%d%y_%H%M%S", time.gmtime()) + ".jpg", "wb") as img:                        
                        img.write(frame)
                        print("Frame",imgNum,"Captured")
                        imgNum  += 1
                        
                if inferIdentity==True:
                    if turingCheck(frame):
                        if indentityCheck(frame):
                            disengageBolt()
                            visitorID = logVisitor()
                            sleep(30)
                            engageBolt()

                    if notificationType==1 or 2:
                        notTimerComp = time.perf_counter()
                        if notTimerComp-notTimerSet >= notDelay:
                            print("Sending Notification")
                            notifyOwner(notificationType, visitorID) #,identityCheck.id)                             ### Create typed notifications
                            notTimerSet = notTimerComp



def handleInput(fields):
    print("Fields:", fields)
    test = str(fields.get('notAdd'))
    print("FieldsValue: ", test)
    if test=="['michael.c.locker@gmail.com']":
        global ownerEmail
        ownerEmail = 'michael.c.locker@gmail.com'
        print("Notification Email Changed to: 'michael.c.locker@gmail.com' ")
    elif test=="['jamedaful@gmail.com']":
        ownerEmail = 'jamedaful@gmail.com'
        print("Notification Email Changed to: 'jamedaful@gmail.com' ")
    elif test=="['notify.lockindustries@gmail.com']":
        ownerEmail = 'notify.lockindustries@gmail.com'
        print("Notification Email Changed to: 'notify.lockindustries@gmail.com' ")
    elif test=="['NotificationMotion']":
        global notificationType
        notificationType = 1
        print("Notifications are now set to motion. ")
    elif test=="['NotificationTuring']":
        notificationType = 2
        print("Notifications are now set to turing. ")
    elif test=="['NotificationOff']":
        notificationType = 0
        print("Notifications are now turned off. ")
    elif test=="['CaptureOn']":
        global captureStillOn
        captureStillOn = True
        print("Still Capturing is now turned on. ")
    elif test=="['CaptureOff']":
        captureStillOn = False
        print("Still Capturing is now turned off. ")
    elif test=="['ExtractImages']":
        extractFiles('/home/pi/CameraProject/','sampleImages','extraction/')
        global imgNum
        imgNum = 0
        print("Extracting Still Images. ") 
    elif test=="['ServerShutdown']":
        global shutdownFlag
        shutdownFlag = 'x'
        print("Server will shutdown")
    else:
        print("Notification Email Not Changed. Invalid Input")
    return


def notifyOwner(notificationSelection, notificationContent=""):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "notify.lockindustries@gmail.com"
    receiver_email = ownerEmail
    #password = input("Type your password and press enter:")
    password = notificationAuth
    message = """\
    Subject: LockCam Notification
    
    """
    if notificationSelection==1 or 2:
        message += """\
        Motion has been detected.

        """
        if notificationContent!='':
            message+= """\
            The subject has been identified as """+notificationContent
        else:
            message+= """\
            The subject cannot be identified. """+notificationContent

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

        
def mse(imageA, imageB):
    # Mean Squared Error sum of the squared 
    # difference will help determine change
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err



class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
#                 camera.annotate_text = ("Captured "+str(imgNum)+" images")
                sequenceCapture()
            self.buffer.seek(0)

        return self.buffer.write(buf)

    
    
class StreamingHandler(server.BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_POST(self):
        print(self.headers)

        content_length = int(self.headers.get('Content-Length', 0))
        content_string = self.rfile.read(content_length).decode("UTF-8")
        fields = parse_qs(content_string)
        handleInput(fields)
        
        self.send_response(302)
        self.send_header('Location', '/index.html')
        self.end_headers()
        self._set_headers()   
        return
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/style.css':
            content = styleSheet.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/javascript.js':
            content = styleSheet.encode('utf-8')
            self.send_response(200)
#             self.send_header('Content-Type', 'text/javascript')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()

            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

            except Exception as e:
                if shutdownFlag=="x":
                    camera.close()
                    server.shutdown()
                    server.server_close()
                    print("Remote Shutdown Requested.")
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

            
            
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    global imgNum

with picamera.PiCamera(resolution='729x729', framerate=24) as camera:
    camera.rotation = 270
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
#    webbrowser.open('http://10.0.0.201:7777', new=0, autoraise=True)
        
    try:
        address = ('', 7777)
        server = StreamingServer(address, StreamingHandler)
        print("Starting Server . . .")
        if notificationType==0:
            print("Notifications are disabled.")
        elif notificationType==1 or 2:
            print("Notifications are set to " + notificationType)
        server.serve_forever() #poll_interval=0.5)
        
    except KeyboardInterrupt:
        camera.close()
        server.shutdown() # Stop the serve_forever
        server.server_close()  # Close also the socket.
        print("Shutdown requested")
        
    except Exception:
        print("Encountered Unhandled Error!")
        camera.close()
        server.shutdown() # Stop the serve_forever
        server.server_close()  # Close also the socket.

    finally:
        camera.close()
        server.shutdown() # Stop the serve_forever
        server.server_close()  # Close also the socket.
