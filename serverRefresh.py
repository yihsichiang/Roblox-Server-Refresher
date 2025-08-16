from tkinter import messagebox
import time
import pyautogui
import cv2
from func import *
import json
import sys
from datetime import datetime


def serverRefresh(isDark=False):
    refresh_img = cv2.imread("image/refresh.png")
    more_img = cv2.imread("image/more.png")
    shutdown_img = cv2.imread("image/shutdown.png")
    
    # press refresh button
    ref_pos = getImagePosOnScreen(refresh_img, isDark)
    if not ref_pos:
        # print("Error: can't find \"refresh\" button.")
        messagebox.showerror("Error", f"Error: can't find \"refresh\" button.")
        return False
    else:
        pyautogui.moveTo(ref_pos[0], ref_pos[1], duration=0.5)
        pyautogui.click()

    time.sleep(5)
    
    # press more button
    more_pos = getImagePosOnScreen(more_img, isDark)
    if not more_pos:
        # print("Error: can't find \"more\" button.")
        messagebox.showerror("Error", f"Error: can't find \"more\" button.")
        return False
    else:
        pyautogui.moveTo(more_pos[0], more_pos[1], duration=0.5)
        pyautogui.click()
        
    time.sleep(5)
    
    # press more button
    shutdown_pos = getImagePosOnScreen(shutdown_img, isDark)
    if not shutdown_pos:
        # print("Error: can't find \"shutdown\" button.")
        messagebox.showerror("Error", f"Error: can't find \"shutdown\" button.")
        return False
    else:
        pyautogui.moveTo(shutdown_pos[0], shutdown_pos[1], duration=0.5)
        pyautogui.click()
        
    return True
        
        
def run_scheduler(app_state):
    # init 
    isDark = app_state["dark_mode"]
    times = app_state["times"]
    time_points = [(int(tp.split(":")[0]), int(tp.split(":")[1]), int(tp.split(":")[2])) for tp in times]
    print(f"isDark: {isDark}")
    print(f"Timeline: {time_points}")
    
    TOLERANCE = 5  # 容錯範圍（秒）
    active = True

    while active:
        now = datetime.now()

        for tp in time_points:
            target = datetime(now.year, now.month, now.day, tp[0], tp[1], tp[2])
            delta = (now - target).total_seconds()

            # 判斷是否在 [0, TOLERANCE] 秒範圍內，且未觸發過
            if 0 <= delta <= TOLERANCE:
                active = serverRefresh(isDark)

        time.sleep(1)
        
        
if __name__ == "__main__":
    app_state = json.loads(sys.argv[1])
    run_scheduler(app_state)