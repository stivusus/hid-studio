import time

class HIDController:
    def __init__(self, port=None):
        self.port = port
        # здесь твоя логика подключения к Arduino

    def connect(self, port):
        self.port = port
        # логика открытия COM-порта

    def press(self, key):
        # отправка команды на Arduino
        print(f"[Arduino] PRESS {key}")

    def release(self, key):
        print(f"[Arduino] RELEASE {key}")

    def click(self, button='left'):
        print(f"[Arduino] CLICK {button}")

    def move(self, dx, dy):
        print(f"[Arduino] MOVE {dx},{dy}")

    def type_text(self, text):
        print(f"[Arduino] TYPE {text}")

    def wait(self, ms):
        time.sleep(ms / 1000)

    def press_and_release(self, key, duration=0.2):
        self.press(key)
        time.sleep(duration)
        self.release(key)

    def combo(self, keys, duration=0.2):
        for k in keys:
            self.press(k)
        time.sleep(duration)
        for k in keys:
            self.release(k)
