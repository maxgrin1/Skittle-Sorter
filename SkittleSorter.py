#Sketch for determening the color of the Skittle and moving servo positions accordingly
#Run calibrate() --> calDone = 0, first and put the gotten values in cal_values = [].
#Sleep() statements should be changed to fit your Skittle Sorter.
#By Luuk van Sundert and Max van Grinsven

from picamera import PiCamera
from colorthief import ColorThief
from scipy import spatial
from time import sleep
import numpy as np
import RPi.GPIO as GPIO
import cv2
#GPIO setup:
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
topServo = GPIO.PWM(11, 50)
bottomServo = GPIO.PWM(12, 50)
topServo.start(8.5)
bottomServo.start(7)
camera = PiCamera()
calDone = 1
#Fill in between the brackets the values gotten from calibrate()
cal_values = [] 
dominant_color = 0
if calDone:
    tree = spatial.KDTree(cal_values)
calString = "Insert "
def getDominantColor():
    camera.capture('maxgrin1.jpg')
    img =  cv2.imread('maxgrin1.jpg', 1)
    cropped = img[340:360, 900:920] #May need to change according to your own Skittle Sorter camera's position.
    cv2.imwrite('maxgrin1_cropped.jpg', cropped)
    color_thief = ColorThief('maxgrin1_cropped.jpg')
    cv2.imshow('test', cropped)
    dominant_color = color_thief.get_color(quality=1)
    print(dominant_color)
    return dominant_color
    
def getSkittle():
    topServo.ChangeDutyCycle(11)
    sleep(1)
    topServo.ChangeDutyCycle(8.5)
    b = tree.query(getDominantColor())
    sleep(0.5)
    if b[1] == 0:
        print ("Red")
        bottomServo.ChangeDutyCycle(3)
    elif b[1] == 1:
        print ("Orange")
        bottomServo.ChangeDutyCycle(4)
    elif b[1] == 2:
        print ("Purple")
        bottomServo.ChangeDutyCycle(5)
    elif b[1] == 3:
        print ("Yellow")
        bottomServo.ChangeDutyCycle(6)
    elif b[1] == 4:
        print ("Green")
        bottomServo.ChangeDutyCycle(7)
    elif b[1] == 5:
        print ("No Skittles left)"
        break
    sleep(0.3)
    topServo.ChangeDutyCycle(3.5)
    sleep(0.5)

def calibrate():
    average = []
    print ("Calibration: insert given color and press any button on keyboard to continue.")
    cv2.waitKey(0)
    for i in range(6):
        if i == 0:
            print (calString + "Red")
            cv2.waitKey(0)
        elif i == 1:
            print (calString + "Orange")
        elif i == 2:
            print (calString + "Purple")
        elif i == 3:
            print (calString + "Yellow")
        elif i == 4:
            print (calString + "Green")
        elif i == 5:
            print (calString + "Empty")
        cv2.waitKey(0)
        for k in range(10): #Range(K) K can be changed, the smaller the faster but less accurate.
            average.append(getDominantColor())
        averages = [sum(vals)/len(average) for vals in zip(*average)]
        averages = [round(x) for x in averages]
        cal_values.append(averages)
        print (i)
        print (cal_values)
    
#The actual sketch itself
if(calDone):
    for a in range(10): #Range(K) K is the amount of Skittles to be sorted.
        getSkittle()
else calibrate()
cv2.destroyAllWindows()
topServo.stop()
bottomServo.stop()
GPIO.cleanup()
