import RPi.GPIO as GPIO
import time

PIN = 17          # BCM 編號：GPIO17（實體腳位 11）
UNIT = 0.2        # 摩斯「一單位」時間（秒），可依需要調整快慢

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

def beep(units: float):
    GPIO.output(PIN, GPIO.HIGH)   # 發聲
    time.sleep(UNIT * units)
    GPIO.output(PIN, GPIO.LOW)    # 靜音
    time.sleep(UNIT)              # 元件間間隔（1 單位）

def morse_SOS():
    # 摩斯規則：
    # dot(·) = 1 單位，dash(—) = 3 單位
    # 同一字母內各元素間隔 1 單位（在 beep() 裡已加）
    # 字母間隔 3 單位（這裡額外補 2 單位，因為前面已休 1）
    # 單字間隔 7 單位（這裡用不到）
    # S = ···
    for _ in range(3):
        beep(1)
    time.sleep(UNIT * 2)  # 補成字母間隔 3 單位

    # O = ———
    for _ in range(3):
        beep(3)
    time.sleep(UNIT * 2)  # 補成字母間隔 3 單位

    # S = ···
    for _ in range(3):
        beep(1)

try:
    while True:
        morse_SOS()
        time.sleep(UNIT * 7)  # 單字間隔（SOS 重複之間留 7 單位）
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()

