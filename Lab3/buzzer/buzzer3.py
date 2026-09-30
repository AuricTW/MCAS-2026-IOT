import RPi.GPIO as GPIO
import time

PIN =   # 接蜂鳴器的腳位

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

# 音階對應的頻率 (Hz)
scale = {
    "Do": 261.6,
    "Re": 293.7,
    "Mi": 329.6,
    "Fa": 349.2,
    "So": 392.0,
    "La": 440.0,
    "Si": 493.9,
    "Do_high": 523.3
}

# 建立 PWM 物件，初始頻率隨便先設一個
buzzer = GPIO.PWM(PIN, 440)

try:
    while True:
        # 依序播放音階
        for note, freq in scale.items():
            print(f"播放 {note} ({freq} Hz)")
            buzzer.ChangeFrequency(freq)  # 設定當前頻率
            buzzer.start(50)              # duty cycle 50%，發聲
            time.sleep(0.5)               # 每個音 0.5 秒
            buzzer.stop()                 # 停止，避免黏音
            time.sleep(0.05)              # 稍微間隔，讓音階更清楚

except KeyboardInterrupt:
    pass
finally:
    buzzer.stop()
    GPIO.cleanup()

