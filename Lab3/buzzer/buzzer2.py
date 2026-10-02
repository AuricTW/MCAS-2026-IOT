import RPi.GPIO as GPIO
import time

PIN2 =        # 實體腳位？？（填你自己的腳位號碼）
freq = 523      # 頻率 (523Hz，大約是 C5)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN2, GPIO.OUT)

# 建立 PWM 物件
voice = GPIO.PWM(PIN2, freq)

try:
    while True:
        for dc in range(0, 101, 5):   # 從 0% 到 100%，每次增加 5%
            voice.start(dc)           # 用不同 duty cycle 發聲
            time.sleep(0.5)           # 停留 0.5 秒

except KeyboardInterrupt:
    pass
finally:
    voice.stop()
    GPIO.cleanup()

