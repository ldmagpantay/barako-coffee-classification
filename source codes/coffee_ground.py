import numpy as np
import coffee_classification as cc
import sklearn
from tkinter import *

directory = 'C:\\Users\\user\\Desktop\\coffee_classification'

classes = ['BARAKO', 'NOT BARAKO']

timer = input('Enter timer (s): ')

def show_output(text_input):

    ws = Tk()
    ws.title('OUTPUT')
 
    #place window in center                                                                                                                  
    scrwdth = ws.winfo_screenwidth()
    scrhgt = ws.winfo_screenheight()
    width = 600
    height = 350
    xLeft = int((scrwdth/2) - (width/2))
    yTop = int((scrhgt/2) - (height/2))

    ws.attributes('-topmost', True)
    ws.geometry(str(width) + "x" + str(height) + "+" + str(xLeft) + "+" + str(yTop))

    ws.iconbitmap(directory + '\\resources\\icons\\coffee-icon.ico')
    Label(
        ws,
        text = text_input,
        bg='white',
        font = ('Arial', 60, 'bold')
        ).pack(fill=BOTH, expand=True)

    ws.mainloop()
#end of function

sensor_inputs = cc.data(directory).enose_run(timer)

#sensor_inputs.append(1)
enose_predictions = cc.process(directory).enose_processing_ground(sensor_inputs)

print(f'Sensor Inputs: {sensor_inputs}\nE-Nose Predictions: {enose_predictions}')

final_output = classes[np.argmax(enose_predictions)]

#show window
show_output(final_output)