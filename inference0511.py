'''
Project Name    :   Plastic Garbage Reduction Project
Project Member  :   Ryota Nakamura
File Name       :   inference0511.py

Function        :   1. garbage input detection
                    2. camera shooting
                    3. recognition of trash documents

Creation Date   :   2022/05/11

Copyright 2021 AAII.
'''

import RPi.GPIO as GPIO             
import time                         
import sys
import os
import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import datetime
import picamera

# Setting GPIO
Trig = 27
Echo = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN) 

# Global variables
count_id = 0
difference_distance = 0
image_recognition_progress = False
image_fileName = None
upload_fileName = None
val_transform = None
model = None

# OK:Plastic bottle
# NG: Not plastic bottle
result = None

# d1:Campus, d2:City, d3:Road along river
# d4:Riverside, d5:Beach with sand, d6:Beach with rocks
# d7:Ocean
difficulty_degree = 'd1' 

LATITUDE = 35.6311 # AAII, Ariake Campus, Tokyo
LONGITUDE = 139.7877
#LATITUDE = 7.8947 # PSU, Facaulty of Technology and Environment
#LONGITUDE = 98.3529

def main():
    preparation_build_inference_model()
    measure()

# Preparation for measurement
def read_distance():
    global Trig,Echo
    GPIO.output(Trig, GPIO.HIGH)            # GPIO27 output=High(3.3V)
    time.sleep(0.00001)                     
    GPIO.output(Trig, GPIO.LOW)             # GPIO27 output=Low(0V)

    while GPIO.input(Echo) == GPIO.LOW:     
        sig_off = time.time()
    while GPIO.input(Echo) == GPIO.HIGH:    
        sig_on = time.time()

    duration = sig_off - sig_on             
    distance = duration * 34000 / 2         # Calculate the distance
    return distance

# Mesure distance with ultrasonic sensor
def measure():
    global image_recognition_progress, difference_distance, count_id
    past_distance = 0
    print("Measurement start...")

    while True:
        try:
            if image_recognition_progress == False:
                # Measure distatnce
                current_distance = read_distance()                  
                current_distance = current_distance * -1

                # print("past_distance:",past_distance)
                # print("current_distance:",current_distance)
                
                if current_distance > 2 and current_distance < 400:               
                    difference_distance =  past_distance - int(current_distance)
                    # print(difference_distance)
                    # if the difference is more than 5cm.
                    if difference_distance > 5 and past_distance != 0:
                        dt_now = datetime.datetime.now()
                        count_id = count_id + 1
                        print("Garbage has been put in. ",dt_now)
                        print("count_id           :", count_id)
                        print("past_distance      :", past_distance,"[cm]")
                        print("current_distance   :",int(current_distance), "[cm]")
                        print("difference_distance:", difference_distance, "[cm]")
                        
                        image_recognition_progress = True
                        capture_photo()
                        inference()

                past_distance = int(current_distance)
                time.sleep(2)                     
                image_recognition_progress = False   

        except KeyboardInterrupt:      
            GPIO.cleanup()             
            print("Mesurement stop...")
            sys.exit()       

def preparation_build_inference_model():
    global val_transform,model
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(), 
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])

    model = models.resnet152() 
    model.fc = nn.Linear(2048,2)
    model_path = 'model0511.pth'
    device = torch.device("cude" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(model_path,map_location=device))
    model.to('cpu')
    model.eval()
    print("OK: preparation inference model")

def capture_photo():
    global image_fileName
    dt_now = datetime.datetime.now()

    with picamera.PiCamera() as camera:
	    # camera.resolution = (2592, 1944)
        camera.resolution = (1280, 720)
        image_fileName = dt_now.strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'

        camera.capture(image_fileName)

def inference():
    global image_fileName, upload_fileName
    global model
    global result,difficulty_degree

    img = Image.open(image_fileName)
    img_transformed = val_transform(img)
    inputs = img_transformed.unsqueeze_(0)
    outputs = model(inputs)
    pred = torch.argmax(outputs, dim=1)

    if pred == 0:
        print('garbage            : NG (Not plastic_bottles)\n')
        result = '_NG_'
    elif pred == 1:
        print('garbage            : OK (plastic_bottles)\n')
        result = '_OK_'

    upload_fileName = (str(difference_distance) + 'cm' 
    + result + image_fileName.split('.')[0] + '_' 
    + difficulty_degree + '_' 
    + 'lat-' + str(LATITUDE) + '_' 
    + 'lon-' + str(LONGITUDE) 
    + '.jpg')
    
    os.rename(image_fileName, upload_fileName)

if __name__ == "__main__":
    main()
