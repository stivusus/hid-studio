import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import serial.tools.list_ports
import parser

root = tk.Tk()
root.title("HID Studio")
root.geometry("480x380")

use_arduino = tk.BooleanVar(value=True)
script = []
hid = None

def get_hid():
    if use_arduino.get():
        import mylib as hidlib
    else:
        import native_hid as hidlib
    return hidlib.HIDController()

def add(cmd):
    script.append(cmd)
    log1.insert(tk.END, cmd + '\n')
    log2.insert(tk.END, cmd + '\n')

def run_script():
    global hid
    if not hid:
        hid = get_hid()
    parser.run_txt_script(script, hid)

def save_script():
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            for line in script:
                f.write(line + '\n')

def load_script():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        script.clear()
        log1.delete(1.0, tk.END)
        log2.delete(1.0, tk.END)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                add(line.strip())

def clear_script():
    script.clear()
    log1.delete(1.0, tk.END)
    log2.delete(1.0, tk.END)

def add_typing():
    text = entry.get()
    if text:
        add(f"TYPE:{text}")
        entry.delete(0, tk.END)

def add_wait():
    ms = simpledialog.askinteger("Пауза", "Введите задержку (мс):", minvalue=0, initialvalue=1000)
    if ms is not None:
        add(f"WAIT:{ms}")

def add_repeat():
    add("REPEAT:?{")
    add("...тут команды...")
    add("}")

def safe_press():
    key = key_entry.get()
    if not key:
        return
    if messagebox.askyesno("Добавить паузу?", f"Добавить RELEASE:{key} и WAIT:500 после PRESS:{key}?"):
        add(f"PRESS:{key}")
        add("WAIT:500")
        add(f"RELEASE:{key}")
    else:
        add(f"PRESS:{key}")

def connect_port():
    global hid
    try:
        hid = get_hid()
        if use_arduino.get():
            hid.connect(com_var.get())
        messagebox.showinfo("Успех", "Контроллер готов")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def refresh_ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    com_var.set(ports[0] if ports else "Нет портов")
    com_menu['menu'].delete(0, 'end')
    for p in ports:
        com_menu['menu'].add_command(label=p, command=lambda value=p: com_var.set(value))

# --- GUI ---
notebook = ttk.Notebook(root)
frame_commands = tk.Frame(notebook)
frame_scripts = tk.Frame(notebook)
frame_arduino = tk.Frame(notebook)

notebook.add(frame_commands, text="Команды")
notebook.add(frame_scripts, text="Сценарии")
notebook.add(frame_arduino, text="Arduino")
notebook.pack(expand=True, fill='both')

# --- Вкладка Команды ---
cmd_grid = tk.Frame(frame_commands)
cmd_grid.pack(pady=10)

tk.Button(cmd_grid, text="Зажать мышь", command=lambda: add("PRESS:MOUSE")).grid(row=0, column=0)
tk.Button(cmd_grid, text="Отпустить мышь", command=lambda: add("RELEASE:MOUSE")).grid(row=0, column=1)
tk.Button(cmd_grid, text="Сдвинуть мышь", command=lambda: add("MOVE:100:0")).grid(row=1, column=0)
tk.Button(cmd_grid, text="Клик мышью", command=lambda: add("CLICK:LEFT")).grid(row=1, column=1)
tk.Button(cmd_grid, text="Пауза", command=add_wait).grid(row=2, column=0)
tk.Button(cmd_grid, text="Цикл", command=add_repeat).grid(row=2, column=1)

# Ввод текста
text_frame = tk.Frame(frame_commands)
text_frame.pack(pady=5)
tk.Button(text_frame, text="Напечатать текст", command=add_typing).pack(side=tk.LEFT)
entry = tk.Entry(text_frame, width=30)
entry.pack(side=tk.LEFT, padx=5)

# Ввод клавиши
key_frame = tk.Frame(frame_commands)
key_frame.pack(pady=5)
key_entry = tk.Entry(key_frame, width=10)
key_entry.pack(side=tk.LEFT)
tk.Button(key_frame, text="Нажать", command=safe_press).pack(side=tk.LEFT)
tk.Button(key_frame, text="Отпустить", command=lambda: add(f"RELEASE:{key_entry.get()}")).pack(side=tk.LEFT)
tk.Button(key_frame, text="Нажать и отпустить", command=lambda: add(f"PRESS:{key_entry.get()}\nWAIT:100\nRELEASE:{key_entry.get()}")).pack(side=tk.LEFT)

# Комбо
combo_frame = tk.Frame(frame_commands)
combo_frame.pack(pady=5)
combo_entry = tk.Entry(combo_frame, width=30)
combo_entry.pack(side=tk.LEFT)
tk.Button(combo_frame, text="Комбо", command=lambda: add(f"COMBO:{combo_entry.get()}")).pack(side=tk.LEFT)

# Поле сценария
log1 = tk.Text(frame_commands, height=10, width=60)
log1.pack(pady=10)

# --- Вкладка Сценарии ---
btn_frame = tk.Frame(frame_scripts)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Загрузить", command=load_script).grid(row=0, column=0, padx=5, pady=2)
tk.Button(btn_frame, text="Сохранить", command=save_script).grid(row=0, column=1, padx=5, pady=2)
tk.Button(btn_frame, text="Запустить", command=run_script).grid(row=1, column=0, padx=5, pady=2)
tk.Button(btn_frame, text="Очистить", command=clear_script).grid(row=1, column=1, padx=5, pady=2)

log2 = tk.Text(frame_scripts, height=10, width=60)
log2.pack(pady=10)

# --- Вкладка Arduino ---
tk.Checkbutton(frame_arduino, text="Без Arduino", variable=use_arduino).pack(pady=5)
com_var = tk.StringVar()
com_menu = tk.OptionMenu(frame_arduino, com_var, "Нет портов")
com_menu.pack()
tk.Button(frame_arduino, text="Обновить порты", command=refresh_ports).pack()
tk.Button(frame_arduino, text="Подключиться", command=connect_port).pack()
refresh_ports()

root.mainloop()
