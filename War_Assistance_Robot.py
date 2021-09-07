import time
import serial
import RPi.GPIO as GPIO
import pygame
import picamera

from time import sleep
from array import array

# import IoTSend
import numpy
import httplib, urllib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import base64
import smtplib

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

usbport = '/dev/ttyS0'
ser = serial.Serial(usbport, 9600)

Metal_Sensor = 16
Gas_Sensor = 18
PIR_Sensor = 15
Motor1 = 36
Motor2 = 37
Motor3 = 38
Motor4 = 40
Laser = 13

Human = ""
Bomb = ""
Gas = ""
GPRS_Tx_Arr = ""
Project_ID = "$234$RRIT$"
email_body = ""
step_count = 0

GPIO.setup(Metal_Sensor, GPIO.IN)
GPIO.setup(PIR_Sensor, GPIO.IN)
GPIO.setup(Gas_Sensor, GPIO.IN)
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)
GPIO.setup(Motor4, GPIO.OUT)
GPIO.setup(Laser, GPIO.OUT)

GPIO.output(Motor1, GPIO.LOW)
GPIO.output(Motor2, GPIO.LOW)
GPIO.output(Motor3, GPIO.LOW)
GPIO.output(Motor4, GPIO.LOW)
GPIO.output(Laser, GPIO.LOW)

GPIO.output(Laser, False)
print("Laser ON")
sleep(3)
GPIO.output(Laser, True)
print("Laser OFF")
sleep(1)

pygame.mixer.init()
pygame.mixer.music.load('3.mp3')
print("Water Sound Play")
pygame.mixer.music.play()
sleep(10)
pygame.mixer.music.stop()
print("Water Sound Stop")


def For():
    GPIO.output(Motor1, True)
    GPIO.output(Motor2, False)
    GPIO.output(Motor3, True)
    GPIO.output(Motor4, False)
    print("FORWARD")
    sleep(4)


##    GPIO.output(Motor1, False)
##    GPIO.output(Motor2, False)
##    GPIO.output(Motor3, False)
##    GPIO.output(Motor4, False)
##    sleep( 2 )

def back():
    GPIO.output(Motor1, False)
    GPIO.output(Motor2, True)
    GPIO.output(Motor3, False)
    GPIO.output(Motor4, True)
    print("BACKWARD")
    sleep(4)


##    GPIO.output(Motor1, False)
##    GPIO.output(Motor2, False)
##    GPIO.output(Motor3, False)
##    GPIO.output(Motor4, False)
##    sleep( 2 )

def right():
    GPIO.output(Motor1, True)
    GPIO.output(Motor2, False)
    GPIO.output(Motor3, False)
    GPIO.output(Motor4, True)
    print("RIGHT")
    sleep(4)


##    GPIO.output(Motor1, False)
##    GPIO.output(Motor2, False)
##    GPIO.output(Motor3, False)
##    GPIO.output(Motor4, False)
##    sleep( 2 )

def left():
    GPIO.output(Motor1, False)
    GPIO.output(Motor2, True)
    GPIO.output(Motor3, True)
    GPIO.output(Motor4, False)
    print("LEFT")
    sleep(4)


##    GPIO.output(Motor1, False)
##    GPIO.output(Motor2, False)
##    GPIO.output(Motor3, False)
##    GPIO.output(Motor4, False)
##    sleep( 2 )
##    


def motoroff():
    GPIO.output(Motor1, False)
    GPIO.output(Motor2, False)
    GPIO.output(Motor3, False)
    GPIO.output(Motor4, False)
    sleep(2)


print("start camera")
camera = picamera.PiCamera()
camera.start_preview()
sleep(5)
camera.stop_preview()
sleep(0.5)
print("stop Camera")

camera.vflip = True
camera.hflip = True
camera.brightness = 60

print("capturing image")
for i in range(0, 2):
    camera.capture('img%02d.jpg' % i, resize=(500, 281))
    sleep(2)

print("capturing image done")


def mail_sent():
    str_from = 'ajaythk.94@gmail.com'
    str_to = 'panchramc1@gmail.com'

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Raspberry pi Evidence image'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msg_text = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    ##        msgText = MIMEText('<b>evidence</b>Check image<br><img src="cid:image1"><br>', 'html')
    msg_text = MIMEText(email_body + '<img src="cid:image1"><br>', 'html')
    msgAlternative.attach(msgText)
    fp = open('img00.jpg', 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image>')
    msgRoot.attach(msgImage)
    u = 'ajaythk.94@gmail.com'
    p = 'gurudev123456789'
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(u, p)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

    print("mail sent successfully")
    sleep(2)


def gprs_init_comm():
    ser.write("AT+CIPSHUT\r")
    sleep(2)
    ser.write("AT+CMGF=1\r")
    sleep(2)

    ser.write("AT+CIPMUX=0\r")
    sleep(2)
    ser.write("AT+CSTT=\"www.airtelgprs.com\",\"\",\"\"\r")
    sleep(7)
    ser.write("AT+CIICR\r")
    sleep(5)
    ser.write("AT+CIFSR\r")
    sleep(5)
    ser.write("AT+CIPSTART=\"TCP\",\"54.214.102.68\",\"85\"\r")
    sleep(8)


def gprs_send_server(gprs_data):
    ser.write("AT+CIPSEND\r")
    sleep(1)
    print("\x1A")  ##cntl+Z
    sleep(0.5)
    ser.write(Gprs_data)
    sleep(3)
    ser.write("\x1A")  ##cntl+Z
    sleep(0.5)
    # Gprs_data =""


ser.write("AT\r")
print("GSM INITIALIZED")
sleep(5)
ser.flushInput()

print("GPRS INIT COMMAND")
Gprs_Init_comm()
print("GPRS INITIALIZED")
sleep(2)
ser.flushInput()

For()
motoroff()
Back()
motoroff()
Left()
motoroff()
Right()
motoroff()

Count_Tx_Delay = 0
step_count = 0
while True:

    print("------------------------------------")

    if step_count == 2:
        Left()

    elif step_count == 4:
        Right()

    else:
        For()

    step_count = step_count + 1
    if step_count >= 8:
        step_count = 0

    if GPIO.input(PIR_Sensor) == True:
        print("HUMAN HAS BEEN DETECTED")
        motoroff()
        Human = 1
        sleep(1)
        GPIO.output(Laser, False)
        print("Laser ON")
        sleep(3)
        GPIO.output(Laser, True)
        print("Laser OFF")
        sleep(1)
    else:
        Human = 0

    if not GPIO.input(Gas_Sensor):
        print("SMOKE HAS BEEN DETECTED")
        motoroff()
        Gas = 1
        print("capturing Smoke image")
        for i in range(0, 2):
            camera.capture('img%02d.jpg' % i, resize=(500, 281))
            sleep(2)
        print("capturing Smoke image done")

        email_body = "GAS HAS BEEN DETECTED"
        Mail_sent()
        sleep(2)

        pygame.mixer.init()
        pygame.mixer.music.load('2.mp3')
        print("SMOKE Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        print("SMOKE Sound Stop")
    else:
        Gas = 0

    if not GPIO.input(Metal_Sensor):
        print("BOMB HAS BEEN DETECTED")
        motoroff()
        Bomb = 1
        print("capturing BOMB image")
        for i in range(0, 2):
            camera.capture('img%02d.jpg' % i, resize=(500, 281))
            sleep(2)
        print("capturing BOMB image done")
        email_body = "BOMB HAS BEEN DETECTED"
        Mail_sent()
        sleep(2)

        pygame.mixer.init()
        pygame.mixer.music.load('1.mp3')
        print("BOMB Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        print("BOMB Sound Stop")
    else:
        Bomb = 0

    GPRS_Tx_Arr = Project_ID + 'H' + str(Human) + 'B' + str(Bomb) + 'G' + str(Gas) + '@'
    print(GPRS_Tx_Arr)
    sleep(4)
    ser.flushInput()

    Count_Tx_Delay = Count_Tx_Delay + 1
    if Count_Tx_Delay >= 6:
        print("Data Update")
        Count_Tx_Delay = 0
        Gprs_Send_Server(GPRS_Tx_Arr)
        sleep(8)
        print("GPRS SENT")
        ser.flushInput()
