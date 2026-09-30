import RPi.GPIO as GPIO
import time

PIN = 11   # 這是「實體腳位 11」 = BCM GPIO11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(PIN, GPIO.HIGH)
        print("LED ON")
        time.sleep(1)
        GPIO.output(PIN, GPIO.LOW)
        print("LED OFF")
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

