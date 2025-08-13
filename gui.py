import tkinter as tk
from threading import Thread
from tkinter import messagebox
import keyboard
import time
import pyautogui
import cv2
from func import *


running = False  # 控制腳本運行狀態


def serverRefresh(interval):
    # init 
    global running
    time.sleep(2)
    refresh_img = cv2.imread("image/refresh.png")
    more_img = cv2.imread("image/more.png")
    shutdown_img = cv2.imread("image/shutdown.png")
    
    while running:
        # press refresh button
        ref_pos = getImagePosOnScreen(refresh_img)
        if not ref_pos:
            # print("Error: can't find \"refresh\" button.")
            messagebox.showerror("Error", f"Error: can't find \"refresh\" button.")
            break
        else:
            pyautogui.moveTo(ref_pos[0], ref_pos[1], duration=0.5)
            pyautogui.click()

        time.sleep(1)
        
        # press more button
        more_pos = getImagePosOnScreen(more_img)
        if not more_pos:
            # print("Error: can't find \"more\" button.")
            messagebox.showerror("Error", f"Error: can't find \"more\" button.")
            break
        else:
            pyautogui.moveTo(more_pos[0], more_pos[1], duration=0.5)
            pyautogui.click()
            
        time.sleep(1)
        
        # press more button
        shutdown_pos = getImagePosOnScreen(shutdown_img)
        if not shutdown_pos:
            # print("Error: can't find \"shutdown\" button.")
            messagebox.showerror("Error", f"Error: can't find \"shutdown\" button.")
            break
        else:
            pyautogui.moveTo(shutdown_pos[0], shutdown_pos[1], duration=0.5)
            pyautogui.click()

        # 等待 t 秒再執行下一次
        time.sleep(interval)
        
    stop_script()


def start_script():
    global running
    if not running:
        running = True
        time_interval = int(hour_spin.get())*3600 + int(min_spin.get())*60 + int(sec_spin.get())
        Thread(target=serverRefresh, args=(time_interval,), daemon=True).start()
        root.iconify()  # 最小化視窗
        print("啟動腳本")


def stop_script():
    global running
    running = False
    root.deiconify()  # 還原視窗
    root.lift()       # 拉到最上層
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    print("腳本已停止")


# 建立 Tkinter 視窗
root = tk.Tk()
root.title("Roblox Server Refresher")
root.geometry("350x200")

# 建立按鈕
start_btn = tk.Button(root, text="Start (F1)", command=start_script, font=("Arial", 14))
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="End (F2)", command=stop_script, font=("Arial", 14))
stop_btn.pack(pady=10)

time_frame = tk.Frame(root)
time_frame.pack(pady=5)

tk.Label(time_frame, text="Time interval to refresh server: ", font=("Arial", 14)).grid(row=0, columnspan=6)

tk.Label(time_frame, text="hour").grid(row=1, column=1)
hour_spin = tk.Spinbox(time_frame, from_=0, to=23, width=5, font=("Arial", 12))
hour_spin.grid(row=1, column=0, padx=5)

tk.Label(time_frame, text="min").grid(row=1, column=3)
min_spin = tk.Spinbox(time_frame, from_=0, to=59, width=5, font=("Arial", 12))
min_spin.grid(row=1, column=2, padx=5)

tk.Label(time_frame, text="sec").grid(row=1, column=5)
sec_spin = tk.Spinbox(time_frame, from_=0, to=59, width=5, font=("Arial", 12))
sec_spin.grid(row=1, column=4, padx=5)

# 註冊熱鍵
keyboard.add_hotkey("F1", start_script)
keyboard.add_hotkey("F2", stop_script)

root.mainloop()
