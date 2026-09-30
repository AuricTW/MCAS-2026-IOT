import RPi.GPIO as GPIO
import time

PIN = 17   # 這是 BCM 編號 (實體腳位 11 對應 GPIO17)
GPIO.setmode(GPIO.BCM)
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

