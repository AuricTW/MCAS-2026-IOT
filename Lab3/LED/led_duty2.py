import RPi.GPIO as GPIO
import time

PIN1 =   # 實體腳位 ？？ (BCM GPIO??)，請依你的接線調整

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN1, GPIO.OUT)

# 建立一個 PWM 物件，頻率固定 100Hz
pwm = GPIO.PWM(PIN1, 100)

try:
    while True:
        for duty in range(0, 101, 10):  # 從 0% → 100%
            pwm.start(duty)             # 設定亮度
            time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

