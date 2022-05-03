import pandas as pd 
import datetime

from Heart_Disease_Scheduler import SmartWatch

#returns the chunk of data within the number of seconds determined by s
#chunks divided by timestamp attribute  
def simulate_data_stream(data, s, next):
    chunk = data.iloc[next:len(df)]

    timestamp = data['timestamp'][next]
    timestamp_new = timestamp + datetime.timedelta(0,s)

    chunk = chunk[chunk['timestamp'] <= timestamp_new]
    
    return chunk  

df = pd.read_csv("./smartwatch.csv")
df = df[df.source.isin(['accelerometer', 'linear_acceleration', 'heart_rate', 'step_counter']) == True]
df = df.sort_values(by='timestamp')
df = df.reset_index(drop=True)
df["timestamp"] = pd.to_datetime(df["timestamp"])

#produces all data within 10 sec 
s = 10
next = 0 
watch = SmartWatch()
while(next<(len(df)-1)):
    chunk=simulate_data_stream(df,s,next)

    heart_rate = chunk[chunk.source.isin(['heart_rate']) == True]
    accelerometer = chunk[chunk.source.isin(['accelerometer']) == True]
    linear_acceleration = chunk[chunk.source.isin(['linear_acceleration']) == True]
    steps = chunk[chunk.source.isin(['step_counter']) == True]

    chunk = chunk.reset_index(drop=True)
    t=chunk['timestamp'][0]

    watch.update(chunk, t)

    next=next+len(chunk)

print("complete")
