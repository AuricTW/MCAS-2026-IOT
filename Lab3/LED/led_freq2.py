import RPi.GPIO as GPIO
import time

PIN1 =   # 實體腳位 ？？ (BCM GPIO??)，請依你的接線調整

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN1, GPIO.OUT)

# 建立一個 PWM 物件，頻率 24Hz
pwm = GPIO.PWM(PIN1, 24)

try:
    while True:
        pwm.start(50)  # duty 固定在 50%，頻率是 24Hz
        time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

