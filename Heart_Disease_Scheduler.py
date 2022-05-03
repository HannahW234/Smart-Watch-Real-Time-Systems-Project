import pandas as pd
from Heart_Disease_Model import Heart_Disease_Model
import datetime

class SmartWatch: 
    def __init__(self):
        self.heart_rates = [] 
        self.accelerometer = []
        self.linear_acceleration = []
        self.steps = []

        self.update_cnt = 0 

        self.model = Heart_Disease_Model()

    def create_model(self, data):
        
        return 0 
    
    def delete_old_data(self, arr, old_timestamp):
        dex = 0 
        for val in arr:
            if(val[0] < old_timestamp):
                arr.pop(dex)
                #print("deleted old data")
            dex = dex+1 
        return arr 

    def evaluate_heart_rate(self):
        heart_rate = 0 
        for value in self.heart_rates:
            v = value[1].strip("']['").split(', ')
            if (float(v[0].strip("'")) > heart_rate):
                heart_rate = float(v[0].strip("'"))
        return heart_rate 
    
    def evaluate_excersize(self):
        #when the sensors for steps, accelerometer, and linear acceleration record
        #we can assume that there is some level of activity 
        #This, with high values determines if there is recent exersize 
        #0 if no excersize, 1 if excersize 
        record_num = len(self.accelerometer) + len(self.linear_acceleration) + len(self.steps)
        steps_num = 0
        for value in self.steps:
            v = value[1].strip("']['").split(', ')
            steps_num = steps_num + float(v[0].strip("'"))

        if(record_num > 10 or steps_num > 30):
            return 1 
        
        return 0  

    def update(self, datastream, t):
        h = datastream[datastream.source.isin(['heart_rate']) == True]
        a = datastream[datastream.source.isin(['accelerometer']) == True]
        l = datastream[datastream.source.isin(['linear_acceleration']) == True]
        s = datastream[datastream.source.isin(['step_counter']) == True]
        
        #updating the data for heart rates and excersize values 
        for index, row in h.iterrows():
                self.heart_rates.append([row['timestamp'], row['values']])

        for index, row in a.iterrows():
                self.accelerometer.append([row['timestamp'], row['values']])

        for index, row in l.iterrows():
                self.linear_acceleration.append([row['timestamp'], row['values']])

        for index, row in s.iterrows():
                self.steps.append([row['timestamp'], row['values']])

        #delete old data 
        old_timestamp = t - datetime.timedelta(0,60)
        self.heart_rates = self.delete_old_data(self.heart_rates, old_timestamp)
        self.accelerometer = self.delete_old_data(self.accelerometer, old_timestamp)
        self.linear_acceleration = self.delete_old_data(self.linear_acceleration, old_timestamp)
        self.steps = self.delete_old_data(self.steps, old_timestamp)

        #get values for prediction 
        heart_rate = self.evaluate_heart_rate()
        excersize = self.evaluate_excersize()

        X_test = [heart_rate, excersize]

        if self.model.predict_heart_disease(X_test): 
            print("ALERT! You may be at risk for heart abnormalities. Please consult a doctor") 
        
        self.update_cnt = self.update_cnt+1 
        return 0
