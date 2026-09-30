import RPi.GPIO as GPIO
import time

PIN =   # 實體腳位？？ (BCM GPIO??)，請依你的接線調整

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

# 建立 PWM 物件，頻率設為 100Hz (夠快，人眼看不到閃爍)
pwm = GPIO.PWM(PIN, 100)
pwm.start(0)  # 一開始 duty = 0%，LED 全暗

try:
    while True:
        # 漸亮
        for duty in range(0, 101, 2):   # 從 0% → 100%
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.02)            # 控制變化速度
        time.sleep(2)                   # 到最亮停 2 秒

        # 漸暗
        for duty in range(100, -1, -2): # 從 100% → 0%
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.02)
        time.sleep(2)                   # 到最暗停 2 秒

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

