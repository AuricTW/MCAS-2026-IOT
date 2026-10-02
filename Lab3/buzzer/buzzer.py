import RPi.GPIO as GPIO
import time

PIN2 =        # 實體腳位？？（填你自己的腳位號碼）
freq = 523      # 頻率 (523Hz，大約是 C5)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN2, GPIO.OUT)

# 建立 PWM 物件，設定頻率 freq
voice = GPIO.PWM(PIN2, freq)

try:
    while True:
        voice.start(50)   # duty 50%，發聲
        time.sleep(1)     # 持續 1 秒
        voice.stop()      # 停止發聲
        time.sleep(1)     # 停 1 秒再響

except KeyboardInterrupt:
    pass
finally:
    voice.stop()
    GPIO.cleanup()

