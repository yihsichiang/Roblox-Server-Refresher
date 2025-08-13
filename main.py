from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ====== 可自訂變數 ======
target_url = "https://www.roblox.com/games/126884695634066/Grow-a-Garden#!/game-instances"   # 你的網頁 URL
time_interval = 60                   # 每隔 t 秒執行一次
button_text = "btn-generic-more-sm"            # 按鈕顯示文字（可改成 id/class）
# ========================

# 啟動 Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service("chromedriver")  # 確保 chromedriver 路徑正確
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打開目標頁面
driver.get(target_url)

while True:
    try:
        # 重新整理網頁
        driver.refresh()

        # 等待按鈕出現（最多等 10 秒）
        wait = WebDriverWait(driver, 10)
        button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//button[contains(text(), '{button_text}')]")
            )
        )

        # 點擊按鈕
        button.click()
        print(f"[{time.strftime('%H:%M:%S')}] 成功點擊按鈕：{button_text}")

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 找不到按鈕或操作失敗：{e}")

    # 等待 t 秒再執行下一次
    time.sleep(time_interval)
