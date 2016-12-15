#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Door Sensor Nick Rowell, Caleb Lemoine

##smtp protocol module for email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

##time module for sleep method
import time

##datetime module for printing date and time on log
import datetime

##GPIO library and create object
import RPi.GPIO as gpio

##subprocess module for calling shell commands
import subprocess

## initialize door
door=0

## initialize count
count=0

## intialize date/time variable
today=(datetime.datetime.now())

##initialize log file
logfile = open("Weekly_Log.txt","a",0)

##Current Date at the top of each daily log
logfile.write("**********")
logfile.write(today.strftime("%m/%d/%Y"))
logfile.write("**********")
logfile.write("\n")
logfile.write("\n")

##email addresses as strings
emailaddr = 'email@gmail.com'

##array of email addresses
addresses = [emailaddr]

## method to email after door has been open for a secified time
def SendEmail():
    fromaddr = "your.email@gmail.com"
    toaddr = addresses

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(addresses)
    msg['Subject'] = "Alert"

    body = "The door wasnt closed all the way"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "your.email.password")
    text = msg.as_string()
    server.sendmail(fromaddr, addresses, text)
    server.quit()

## set GPIO mode to BCM
## this takes GPIO number instead of pin number
gpio.setmode(gpio.BCM)

##LED
led = 21
gpio.setup(led, gpio.OUT)

##specified pin number to read from
door_pin = 23

## use the built-in pull-up resistor
gpio.setup(door_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # activate input with PullUp


## this loop will execute the if statement that is true
try:
	##LED on
	gpio.output(led, True)
        while True:

    ## if the switch is open
            if gpio.input(door_pin):
                now=(datetime.datetime.now())
                logfile.write("Door Opened    ")
                logfile.write(now.strftime("%m/%d/%Y   %H:%M:%S"))
                logfile.write("\n")
                ##play alert sound file
                subprocess.call(['aplay alertshort.wav'],shell=True)
                time.sleep(5)
                count=count + 1
                if count >= 50:
                    SendEmail()
                    logfile.write("Door has been open for 5 minutes")
                    count=0

                ## if the switch is closed
                if (gpio.input(door_pin)==False):
                    time.sleep(1)
                    count=0
except:
	gpio.output(led, False)
