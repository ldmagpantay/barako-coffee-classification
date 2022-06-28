# DESIGN AND DEVELOPMENT OF BARAKO COFFEE CLASSIFICATION USING ELECTRONIC NOSE
# AND TRANSFER LEARNING-BASED DEEP CONVOLUTIONAL NEURAL NETWORK

#import necessary modules
import cv2 
import os
import time as t
import tensorflow as tf
import numpy as np
import pandas as pd
import serial 
import pickle
import schedule as sched
import sklearn

from tkinter import * 
from tkinter import font
from PIL import Image
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

ser = serial.Serial('COM4', 9600) #Arduino must be connected, change the port number if necessary
ser.close()
ser.open()

class data:

    def __init__(self, directory):
        
        self.directory = directory
        
        self.mq2_values = []
        self.mq7_values = []
        self.mq135_values = []
        self.mq137_values = []
        self.counter = 0
    
    def get_sensorData(self):

        arduino_data = ser.readline()

        value_list = [] #storage of sensor data

        decoded_values = str(arduino_data[0:len(arduino_data)].decode('UTF-8'))
        list_values = decoded_values.split('x')
        
        for values in list_values:
            value_list.append(int(values)) 
        print(f'{self.counter}: {value_list}')

        self.mq2_values.append(value_list[0]) 
        self.mq7_values.append(value_list[1])
        self.mq135_values.append(value_list[2]) 
        self.mq137_values.append(value_list[3])
    #end of function

    def enose_run(self, timer):

        flag = True
        sched.every(1).seconds.do(self.get_sensorData)

        while flag:
            sched.run_pending()
            t.sleep(1)
            
            self.counter = self.counter+1
            if self.counter == timer:
                flag = False
                ser.close()
        #end of while

        sensorData = {'MQ-2 Values': self.mq2_values, 
                    'MQ-7 Values': self.mq7_values, 
                    'MQ-135 Values': self.mq135_values, 
                    'MQ-137 Values': self.mq137_values} #create a dictionary of gathered data
        print('DONE AFTER ' + str(len(self.mq2_values)) + ' s\n')

        df = pd.DataFrame(sensorData)
        df.to_csv(self.directory + '/resources/enose gathered data/gathered data.csv')

        mq2_average = int(np.average(self.mq2_values))
        mq7_average = int(np.average(self.mq7_values))
        mq135_average = int(np.average(self.mq135_values))
        mq137_average = int(np.average(self.mq137_values))

        sensor_inputs = [mq2_average, 
                        mq7_average, 
                        mq135_average, 
                        mq137_average]

        return sensor_inputs
    #end of function

    def capture_img(self):

        cam = cv2.VideoCapture(0)
        img_name = 'captured image.jpg'

        while True:
            ret, frame = cam.read()
            if not ret: #check if camera/webcam is working or detected
                print('Failed to grab frame!')
                break

            print('Wait for 3 seconds.')
            for i in range(3):
                print(f'{3-i}')
                t.sleep(1)
            #end of timer

            cv2.imshow('Captured Image', frame)
            cv2.waitKey(3000)
            cv2.imwrite(os.path.join(self.directory + '/resources/captured images', img_name), frame) #save captured image
            print('{} saved!'.format(img_name))
            break
        #end of while
        img_input = self.directory + '/resources/captured images/captured image.jpg'
        cam.release()
        cv2.destroyAllWindows()
        return img_input
    #end of function
#end of class

class process:

    def __init__(self, directory):
        
        self.directory = directory
        self.machineLearning_model_beans = pickle.load(open(directory + '/models/eNose_model_lr_beans.sav', 'rb')) #load the machine learning model
        self.machineLearning_model_ground = pickle.load(open(directory + '/models/eNose_model_lr_ground.sav', 'rb')) 
        self.deepLearning_model = tf.keras.models.load_model(directory + '/models/MobileNetV2.h5') #load the deep learning model
    
    def enose_processing_beans(self, enose_inputs):

        machineLearning_model_beans = self.machineLearning_model_beans
        enose_inputs = (np.array(enose_inputs)).reshape(1,-1)

        enose_predictions = machineLearning_model_beans.predict_proba(enose_inputs)
        return enose_predictions
    #end of function

    def enose_processing_ground(self, enose_inputs):

        machineLearning_model_ground = self.machineLearning_model_ground
        enose_inputs = (np.array(enose_inputs)).reshape(1,-1)

        enose_predictions = machineLearning_model_ground.predict_proba(enose_inputs)
        return enose_predictions
    #end of function

    def img_processing(self, img_to_load):

        deepLearning_model = self.deepLearning_model

        img_input = load_img(img_to_load, target_size=(224,224)) #load image input
                        
        #preprocess captured image
        img = img_to_array(img_input)
        img_batch = np.expand_dims(img, axis=0)
        img_preprocessed = preprocess_input(img_batch)

        img_prediction = deepLearning_model.predict(img_preprocessed)
        return img_prediction
    #end of function

    def softVoter(self, cl1_barako, cl1_notBarako, cl2_barako, cl2_notBarako):

      barako = ((cl1_barako)*50) + ((cl2_barako)*50)
      notBarako = ((cl1_notBarako)*50) + ((cl2_notBarako)*50)
      
      return barako
    #end of function
#end of class