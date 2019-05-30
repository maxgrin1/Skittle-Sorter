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
#Red, Orange, Purple, Yellow, Green
calDone = 1
cal_values = [[129, 37, 44], [134, 48, 48], [104, 39, 40], [112, 54, 46], [95, 57, 42]]
dominant_color = 0
tree = spatial.KDTree(cal_values)
calString = "Insert "
def getDominantColor():
    camera.capture('maxgrin1.jpg')
    img =  cv2.imread('maxgrin1.jpg', 1)

    cropped = img[340:360, 900:920] #Values need to be changed later
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
    sleep(0.3)
    topServo.ChangeDutyCycle(3.5)
    sleep(0.5)

def calibrate():
    average = []
    print ("Calibration: insert given color and press any button on keyboard to continue.")
    cv2.waitKey(0)
    for i in range(5):
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
        cv2.waitKey(0)
        for k in range(10):
            average.append(getDominantColor())
        averages = [sum(vals)/len(average) for vals in zip(*average)]
        averages = [round(x) for x in averages]
        cal_values.append(averages)
        print (i)
        print (cal_values)
    
#The actual sketch itself
if(calDone):
    for a in range(10):
        getSkittle()

cv2.destroyAllWindows()
topServo.stop()
GPIO.cleanup()
