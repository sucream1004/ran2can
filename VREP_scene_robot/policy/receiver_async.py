import vrep,time,sys
import matplotlib.pyplot as plt
from PIL import Image as I
import numpy as np

def streamVisionSensor(visionSensorName,clientID,pause=0.0001):
    #Get the handle of the vision sensor
    res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
    #Get the image
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
    #Initialiazation of the figure
    time.sleep(0.5)
    res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
    im = I.new("RGB", (resolution[0], resolution[1]), "white")
    # Init figure
    plt.ion()
    fig = plt.figure(1)
    plotimg = plt.imshow(im, origin='lower')
    #Let some time to Vrep in order to let him send the first image, otherwise the loop will start with an empty image and will crash
    time.sleep(1)
    c = 0
    while (vrep.simxGetConnectionId(clientID)!=-1): 
        #Get the image of the vision sensor
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
        #Transform the image so it can be displayed
        img = np.array(image,dtype=np.uint8).reshape([resolution[1],resolution[0],3])
        #Update the image
        fig.canvas.set_window_title(visionSensorName + '_' + str(c))
        plotimg.set_data(img)
        plt.draw()
        plt.pause(pause)
        c+=1
    print('End of Simulation')
    
if __name__ == '__main__':
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        streamVisionSensor('cam_1_tex',clientID,0.0001)

    else:
        print('Connection non successful')
        sys.exit('Could not connect')