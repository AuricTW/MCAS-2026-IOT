import RPi.GPIO as GPIO
import time

PIN =   # 實體腳位 ？？ (BCM GPIO??)，請依你的接線調整
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

try:
    pwm = GPIO.PWM(PIN, 1)  # 一開始頻率 1Hz
    pwm.start(50)           # duty 固定 50% (亮一半，暗一半)

    while True:
        for freq in [1, 5, 10, 50, 100, 500]:
            pwm.ChangeFrequency(freq)
            print(f"現在頻率 = {freq} Hz")
            time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

