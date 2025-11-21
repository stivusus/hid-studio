import pyautogui
import keyboard
import time

class HIDController:
    def press(self, key):
        keyboard.press(key)

    def release(self, key):
        keyboard.release(key)

    def click(self, button='left'):
        pyautogui.click(button=button)

    def move(self, dx, dy):
        x, y = pyautogui.position()
        pyautogui.moveTo(x + dx, y + dy)

    def scroll(self, amount):
        pyautogui.scroll(amount)

    def type_text(self, text):
        pyautogui.write(text)

    def wait(self, ms):
        time.sleep(ms / 1000)

    def connect(self, port=None):
        pass  # для совместимости с Arduino-режимом
