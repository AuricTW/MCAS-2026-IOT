import RPi.GPIO as GPIO
import time

PIN =   # 實體腳位 ？？ (BCM GPIO??)，請依你的接線調整
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

try:
    pwm = GPIO.PWM(PIN, 100)  # 頻率固定 100Hz
    pwm.start(0)              # duty 一開始是 0% (全暗)

    while True:
        # 漸亮
        for duty in range(0, 101, 5):  # 0% → 100%
            pwm.ChangeDutyCycle(duty)
            print(f"Duty = {duty}%")
            time.sleep(0.05)

        # 漸暗
        for duty in range(100, -1, -5):  # 100% → 0%
            pwm.ChangeDutyCycle(duty)
            print(f"Duty = {duty}%")
            time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

