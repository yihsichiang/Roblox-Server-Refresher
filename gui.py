import tkinter as tk
import json
import os
from threading import Thread
import keyboard
import signal
import sys
import subprocess
from timeEntry import *
from serverRefresh import *


SETTINGS_FILE = "settings.json"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # 建立 Tkinter 視窗
        self.title("Roblox Server Refresher")
        self.geometry("450x350")
        self.resizable(False, False)

        self.buildStartEndButton()
        self.buildDarkSelect()
        self.buildTimeList()
        
        # 載入設定
        self.load_settings()

        # 關閉視窗時存檔
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.script_process = None

        # 註冊熱鍵
        keyboard.add_hotkey("F1", self.start_script)
        keyboard.add_hotkey("F2", self.stop_script)
        
    
    def buildStartEndButton(self):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        
        # 建立按鈕
        start_btn = tk.Button(frame, text="Start (F1)", command=self.start_script, font=("Arial", 14))
        start_btn.grid(row=0, column=0)

        stop_btn = tk.Button(frame, text="End (F2)", command=self.stop_script, font=("Arial", 14))
        stop_btn.grid(row=0, column=1)
        
        
    def buildTimeList(self):
        self.timeFrame = tk.Frame(self)
        self.timeFrame.pack(pady=5)
        
        self.time_entries = []
        
        # === 加入滾動區域 ===
        container = tk.LabelFrame(self.timeFrame, text="Timeline", relief="solid", borderwidth=1, font=("Arial", 14))
        container.grid(row=0, column=0, pady=5)

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(container, height=150)  # 視窗高度可調
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 加號按鈕
        add_btn = tk.Button(self.timeFrame, text="+ Add timeline", command=self.add_time_entry, font=("Arial", 14))
        add_btn.grid(row=1, column=0, pady=5)

        # 測試用：顯示目前所有時間點
        # show_btn = tk.Button(self.timeFrame, text="顯示時間列表", command=self.show_times, font=("Arial", 14))
        # show_btn.grid(row=2, column=0, pady=5)
        
        
    def buildDarkSelect(self):
        dark_frame = tk.Frame(self)
        dark_frame.pack(pady=5)

        self.isDark = tk.BooleanVar(value=False)
        
        dark_mode_checkbox = tk.Checkbutton(
            dark_frame, 
            text="Dark mode", 
            variable=self.isDark,
            font=("Arial", 14)
        )
        dark_mode_checkbox.grid(row=0, column=0, padx=10, sticky="w")
        
        self.isDark.trace_add("write", lambda *a: self.save_settings())
        
        
    def add_time_entry(self, time_str="00:00:00"):
        entry = TimeEntry(
            self.scrollable_frame,
            on_change_callback=self.save_settings,
            remove_callback=lambda e=None: self.remove_time_entry(entry)
        )
        entry.set_time(time_str)
        self.time_entries.append(entry)
        self.refresh_entries()
        self.save_settings()

    def remove_time_entry(self, entry):
        self.time_entries.remove(entry)
        entry.destroy()
        self.refresh_entries()
        self.save_settings()

    def refresh_entries(self):
        for idx, entry in enumerate(self.time_entries):
            entry.grid(row=idx, column=0, pady=2, sticky="w")
            entry.set_label(idx)


    def get_all_times(self):
        return [entry.get_time_str() for entry in self.time_entries]
    
    
    def get_all_states(self):
        state = {
            "dark_mode": self.isDark.get(),
            "times": self.get_all_times()
        }
        return state


    def save_settings(self):
        data = {
            "dark_mode": self.isDark.get(),
            "times": self.get_all_times()
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.isDark.set(data.get("dark_mode", False))
            for t in data.get("times", []):
                self.add_time_entry(t)


    def on_close(self):
        self.save_settings()
        self.kill_subprocess()
        self.destroy()


    def start_script(self):
        if self.script_process is not None:
            return
        print("Start triggered")
        self.iconify()
        
        def run_script():
            self.script_process = subprocess.Popen(
                [sys.executable, "serverRefresh.py", json.dumps(self.get_all_states())],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            self.script_process.wait()
            self.script_process = None
            self.stop_script()
            
        Thread(target=run_script, daemon=True).start()


    def stop_script(self):
        print("End triggered")
        self.kill_subprocess()
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)
        self.after(500, lambda: self.attributes("-topmost", False))
        
        
    def kill_subprocess(self):
        if self.script_process is not None:
            self.script_process.send_signal(signal.CTRL_BREAK_EVENT)
            self.script_process = None


if __name__ == "__main__":
    app = App()
    app.mainloop()