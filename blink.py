import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

GPIO.output(25,False)
GPIO.output(21,False)
