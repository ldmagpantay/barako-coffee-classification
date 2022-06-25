from msilib import Directory
import numpy as np
import coffee_classification as cc
from tkinter import *

directory = 'C:\\Users\\user\\Desktop\\coffee_classification' #change the directory

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

    ws.iconbitmap(directory + '\resources\icons\coffee-bean-icon.ico')
    Label(
        ws,
        text = text_input,
        bg='white',
        font = ('Arial', 60, 'bold')
        ).pack(fill=BOTH, expand=True)

    ws.mainloop()
#end of function

#gather inputs
sensor_inputs = cc.data(directory).enose_run(timer)
img_input = cc.data(directory).capture_img()

#processing of inputs
enose_predictions = cc.process(directory).enose_processing_beans(sensor_inputs)
img_predictions = cc.process(directory).img_processing(img_input) #input the directory of the image input

print(f'E-Nose Prediciton: {enose_predictions}\nImage Predictions: {img_predictions}')
final_output_ind = cc.process(directory).softVoter(enose_predictions[0][0], 
                                          enose_predictions[0][1], 
                                          img_predictions[0][0], 
                                          img_predictions[0][1])

final_output = classes[final_output_ind]
#final_output = classes[np.argmax(img_predictions)]
print(f'Final Decision: {final_output}')

#show window
show_output(final_output)