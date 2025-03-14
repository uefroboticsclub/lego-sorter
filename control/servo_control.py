import RPi.GPIO as GPIO
import time

SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

def move_paddle():
    servo.ChangeDutyCycle(7)
    time.sleep(0.5)
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)

servo.stop()
GPIO.cleanup()