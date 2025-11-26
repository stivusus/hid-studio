#include <Keyboard.h>
#include <Mouse.h>

// HID Studio Arduino sketch
// Управляет клавиатурой и мышью через команды по Serial

void setup() {
  Serial.begin(9600);
  Keyboard.begin();
  Mouse.begin();
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("K:")) {
      handleKeyboard(cmd.substring(2));
    } else if (cmd.startsWith("M:")) {
      handleMouse(cmd.substring(2));
    }
  }
}

// -------------------- KEYBOARD --------------------
void handleKeyboard(String kcmd) {
  if (kcmd.startsWith("PRESS:")) {
    String key = kcmd.substring(6);
    sendKey(key, true);
  } else if (kcmd.startsWith("RELEASE:")) {
    String key = kcmd.substring(8);
    sendKey(key, false);
  }
}

void sendKey(String key, bool press) {
  key.toUpperCase();

  if (key == "CTRL") press ? Keyboard.press(KEY_LEFT_CTRL) : Keyboard.release(KEY_LEFT_CTRL);
  else if (key == "ALT") press ? Keyboard.press(KEY_LEFT_ALT) : Keyboard.release(KEY_LEFT_ALT);
  else if (key == "SHIFT") press ? Keyboard.press(KEY_LEFT_SHIFT) : Keyboard.release(KEY_LEFT_SHIFT);
  else if (key == "GUI") press ? Keyboard.press(KEY_LEFT_GUI) : Keyboard.release(KEY_LEFT_GUI);
  else if (key == "ENTER") press ? Keyboard.press(KEY_RETURN) : Keyboard.release(KEY_RETURN);
  else if (key == "TAB") press ? Keyboard.press(KEY_TAB) : Keyboard.release(KEY_TAB);
  else if (key == "ESC") press ? Keyboard.press(KEY_ESC) : Keyboard.release(KEY_ESC);
  else if (key == "SPACE") press ? Keyboard.press(' ') : Keyboard.release(' ');
  else if (key == "BACKSPACE") press ? Keyboard.press(KEY_BACKSPACE) : Keyboard.release(KEY_BACKSPACE);
  else if (key == "DELETE") press ? Keyboard.press(KEY_DELETE) : Keyboard.release(KEY_DELETE);
  else if (key == "UP") press ? Keyboard.press(KEY_UP_ARROW) : Keyboard.release(KEY_UP_ARROW);
  else if (key == "DOWN") press ? Keyboard.press(KEY_DOWN_ARROW) : Keyboard.release(KEY_DOWN_ARROW);
  else if (key == "LEFT") press ? Keyboard.press(KEY_LEFT_ARROW) : Keyboard.release(KEY_LEFT_ARROW);
  else if (key == "RIGHT") press ? Keyboard.press(KEY_RIGHT_ARROW) : Keyboard.release(KEY_RIGHT_ARROW);
  else if (key.startsWith("F")) {
    int fn = key.substring(1).toInt();
    if (fn >= 1 && fn <= 12) {
      press ? Keyboard.press(KEY_F1 + fn - 1) : Keyboard.release(KEY_F1 + fn - 1);
    }
  }
  else if (key.length() == 1) {
    char c = key.charAt(0);
    press ? Keyboard.press(c) : Keyboard.release(c);
  }
}

// -------------------- MOUSE --------------------
void handleMouse(String mcmd) {
  if (mcmd.startsWith("CLICK:")) {
    String btn = mcmd.substring(6);
    if (btn == "LEFT") Mouse.click(MOUSE_LEFT);
    else if (btn == "RIGHT") Mouse.click(MOUSE_RIGHT);
    else if (btn == "MIDDLE") Mouse.click(MOUSE_MIDDLE);
  } else if (mcmd.startsWith("MOVE:")) {
    int sep = mcmd.indexOf(':', 5);
    int dx = mcmd.substring(5, sep).toInt();
    int dy = mcmd.substring(sep + 1).toInt();
    Mouse.move(dx, dy);
  } else if (mcmd.startsWith("SCROLL:")) {
    int amount = mcmd.substring(7).toInt();
    Mouse.move(0, 0, amount); // прокрутка
  } else if (mcmd.startsWith("PRESS:")) {
    String btn = mcmd.substring(6);
    if (btn == "LEFT") Mouse.press(MOUSE_LEFT);
    else if (btn == "RIGHT") Mouse.press(MOUSE_RIGHT);
    else if (btn == "MIDDLE") Mouse.press(MOUSE_MIDDLE);
  } else if (mcmd.startsWith("RELEASE:")) {
    String btn = mcmd.substring(8);
    if (btn == "LEFT") Mouse.release(MOUSE_LEFT);
    else if (btn == "RIGHT") Mouse.release(MOUSE_RIGHT);
    else if (btn == "MIDDLE") Mouse.release(MOUSE_MIDDLE);
  }
}
