import serial
import time

# Подключение к Arduino (замени COM3 на свой порт)
arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)

def send_command(cmd: str):
    """Отправка команды в Arduino"""
    arduino.write((cmd + "\n").encode())
    time.sleep(0.05)  # небольшая пауза

# -------------------- Примеры --------------------

# Нажать и отпустить ENTER
send_command("K:PRESS:ENTER")
time.sleep(0.1)
send_command("K:RELEASE:ENTER")

# Напечатать букву A
send_command("K:PRESS:A")
time.sleep(0.05)
send_command("K:RELEASE:A")

# Клик мышью
send_command("M:CLICK:LEFT")

# Переместить мышь на +50 по X и +20 по Y
send_command("M:MOVE:50:20")

# Прокрутить колесо мыши вниз
send_command("M:SCROLL:-3")
