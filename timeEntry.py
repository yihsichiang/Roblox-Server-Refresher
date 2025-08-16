import tkinter as tk


class TimeEntry(tk.Frame):
    def __init__(self, master, on_change_callback, remove_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_change_callback = on_change_callback
        self.remove_callback = remove_callback

        # 時間標籤
        self.label = tk.Label(self, text="Time ?")
        self.label.grid(row=0, column=0, padx=5)

        # hour
        self.hour_var = tk.StringVar(value="00")
        self.hour_spin = tk.Spinbox(self, from_=0, to=23, wrap=True, width=3,
                                    textvariable=self.hour_var, format="%02.0f",
                                    command=self.on_change_callback,
                                    state="readonly")
        self.hour_spin.grid(row=0, column=1)

        # min
        self.min_var = tk.StringVar(value="00")
        self.min_spin = tk.Spinbox(self, from_=0, to=59, wrap=True, width=3,
                                   textvariable=self.min_var, format="%02.0f",
                                   command=self.on_change_callback,
                                   state="readonly")
        self.min_spin.grid(row=0, column=3)

        # sec
        self.sec_var = tk.StringVar(value="00")
        self.sec_spin = tk.Spinbox(self, from_=0, to=59, wrap=True, width=3,
                                   textvariable=self.sec_var, format="%02.0f",
                                   command=self.on_change_callback,
                                   state="readonly")
        self.sec_spin.grid(row=0, column=5)

        # ":" 分隔
        tk.Label(self, text=":").grid(row=0, column=2, sticky="w")
        tk.Label(self, text=":").grid(row=0, column=4, sticky="w")

        # 刪除按鈕
        self.remove_button = tk.Button(self, text="x", width=3, command=self.remove_callback)
        self.remove_button.grid(row=0, column=6, padx=5)

        # 綁定變數改變事件 (手動輸入時也能觸發)
        self.hour_var.trace_add("write", lambda *a: self.on_change_callback())
        self.min_var.trace_add("write", lambda *a: self.on_change_callback())
        self.sec_var.trace_add("write", lambda *a: self.on_change_callback())

    def get_time_str(self):
        return f"{int(self.hour_var.get()):02d}:{int(self.min_var.get()):02d}:{int(self.sec_var.get()):02d}"

    def set_time(self, time_str):
        h, m, s = map(int, time_str.split(":"))
        self.hour_var.set(f"{h:02d}")
        self.min_var.set(f"{m:02d}")
        self.sec_var.set(f"{s:02d}")

    def set_label(self, index):
        self.label.config(text=f"Time {index+1}")