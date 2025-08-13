import pyautogui
import cv2
import numpy as np


def getImagePosOnScreen(img):
    # 擷取螢幕
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 模板比對
    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 判斷最佳位置
    threshold = 0.8  # 相似度閾值，可自行調整
    if max_val >= threshold:
        top_left = max_loc
        h, w = img.shape[:2]
        pos = (top_left[0] + w/2, top_left[1] + h/2)
        
        return pos

    else:
        return None