import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import string
from threading import Thread
from datetime import datetime
import os
import datetime as dt
import winsound
import subprocess
import sys

try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
except ImportError:
    toaster = None
    print("win10toast 설치시 윈도우 알림 가능 (pip install win10toast)")

class AutoClosePopup(tk.Toplevel):
    def __init__(self, master, message, duration=3000):
        super().__init__(master)
        self.title("WARNING")
        self.configure(bg="yellow")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        label = tk.Label(self, text=message, bg="yellow", fg="red", font=("Arial", 12, "bold"))
        label.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        close_btn = tk.Button(self, text="Close", command=self.destroy)
        close_btn.pack(pady=(0,10))

        popup_width = 300
        popup_height = 120
        self.geometry(f"{popup_width}x{popup_height}")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = random.randint(0, screen_width - popup_width)
        y = random.randint(0, screen_height - popup_height)

        self.geometry(f"+{x}+{y}")
        self.attributes("-topmost", True)
        self.after(duration, self.destroy)

class FakeHackerGUI:
    def __init__(self, root):
        self.root = root
        # 수정된 부분: is_user 포함해서 받기
        self.window_title, self.version, self.is_beta, self.is_user = self.load_version_info()
        self.root.title(self.window_title)
        self.root.geometry("900x650")
        self.fullscreen = False
        self.root.configure(bg="black")
        self.root.bind("<F11>", self.toggle_fullscreen)

        self.running = False
        self.current_theme = "dark"
        self.custom_messages = []

        self.attack_modes = ["Brute Force", "DDoS", "SQL Injection"]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_dir = os.path.join(base_dir, "LOGS")
        os.makedirs(self.log_dir, exist_ok=True)
        today_str = dt.datetime.now().strftime("%Y%m%d")
        self.log_file_name = f"{self.version}_{today_str}_user.log"
        self.log_file_path = os.path.join(self.log_dir, self.log_file_name)
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w", encoding="utf-8") as f:
                f.write(f"[INFO] App version: {self.version}, beta: {self.is_beta}, user_ver: {self.is_user}\n")

        self.create_widgets()
        self.load_custom_messages()

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg="black")
        top_frame.pack(pady=5, fill=tk.X)

        tk.Label(top_frame, text="Attack Mode:", fg="lime", bg="black", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(10,5))
        self.attack_mode_var = tk.StringVar(value=self.attack_modes[0])
        self.attack_combo = ttk.Combobox(top_frame, values=self.attack_modes, textvariable=self.attack_mode_var, state="readonly", width=15)
        self.attack_combo.pack(side=tk.LEFT)

        self.theme_btn = tk.Button(top_frame, text="Toggle Theme", command=self.toggle_theme, bg="gray", fg="white")
        self.theme_btn.pack(side=tk.LEFT, padx=10)

        self.open_log_btn = tk.Button(top_frame, text="Open Log", command=self.open_log_file, bg="blue", fg="white")
        self.open_log_btn.pack(side=tk.LEFT, padx=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        self.text_area = tk.Text(
            self.root, bg="black", fg="lime", insertbackground="lime",
            font=("Courier", 12), wrap=tk.WORD, state=tk.DISABLED
        )
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10)

        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start Hacking", command=self.start_hacking, bg="green", fg="black", width=12)
        self.start_button.pack(side=tk.LEFT, padx=8)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_hacking, bg="red", fg="white", width=12)
        self.stop_button.pack(side=tk.LEFT, padx=8)

        self.clear_button = tk.Button(button_frame, text="Clear (CLS)", command=self.clear_text, bg="gray", fg="white", width=12)
        self.clear_button.pack(side=tk.LEFT, padx=8)

    def load_version_info(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        version_file = os.path.join(base_dir, "versions", "version.txt")

        version = "v?.?"
        is_beta = False
        is_user = False

        if os.path.exists(version_file):
            try:
                with open(version_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("version="):
                            version = line.strip().split("=", 1)[1]
                        elif line.startswith("beta_version="):
                            is_beta = line.strip().split("=", 1)[1].lower() == "true"
                        elif line.startswith("user_ver="):
                            is_user = line.strip().split("=", 1)[1].lower() == "true"
            except Exception as e:
                print(f"version.txt 읽기 실패: {e}")
        else:
            print("version.txt 파일이 없습니다!")

        tags = []
        if is_beta:
            tags.append("beta")
        if is_user:
            tags.append("사용자 지정")

        tag_str = f"[{', '.join(tags)}]" if tags else ""
        window_title = f"Hacking_app_{version}{tag_str}"

        return window_title, version, is_beta, is_user

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.apply_light_theme()
        else:
            self.current_theme = "dark"
            self.apply_dark_theme()

    def apply_light_theme(self):
        self.root.configure(bg="white")
        self.text_area.config(bg="white", fg="black", insertbackground="black")
        self.progress.config(style="Light.Horizontal.TProgressbar")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg="white")
                for child in widget.winfo_children():
                    if isinstance(child, (tk.Button, tk.Label)):
                        child.config(bg="white", fg="black")

    def apply_dark_theme(self):
        self.root.configure(bg="black")
        self.text_area.config(bg="black", fg="lime", insertbackground="lime")
        self.progress.config(style="Dark.Horizontal.TProgressbar")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg="black")
                for child in widget.winfo_children():
                    if isinstance(child, (tk.Button, tk.Label)):
                        child.config(bg="black", fg="lime")

    def start_hacking(self):
        if not self.running:
            self.running = True
            self.root.title("Hacking...")
            self.root.config(cursor="watch")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            Thread(target=self.run_hacking_sequence, daemon=True).start()

    def stop_hacking(self):
        if self.running:
            self.running = False
            self.append_text("[SYSTEM] Hacking stopping...")
            self.root.title("Stopping...")
            self.root.config(cursor="arrow")
            self.stop_button.config(state=tk.DISABLED)
            self.root.after(500, self.finish_stop)

    def finish_stop(self):
        self.root.title(self.window_title)
        self.progress['value'] = 0
        self.start_button.config(state=tk.NORMAL)

    def clear_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)

    def load_custom_messages(self):
        self.custom_messages = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        messages_path = os.path.join(base_dir, "settings", "messages.txt")
        if os.path.exists(messages_path):
            try:
                with open(messages_path, "r", encoding="utf-8") as f:
                    self.custom_messages = [line.strip() for line in f if line.strip()]
                print(f"사용자 메시지 {len(self.custom_messages)}개 로드됨")
            except Exception as e:
                print(f"사용자 메시지 로드 실패: {e}")

    def run_hacking_sequence(self):
        self.simulate_loading()
        self.generate_fake_progress()
        self.run_fake_messages()

    def simulate_loading(self):
        loading_text = ["[.] Loading modules", "[..] Initializing network", "[...] Connecting..."]
        for i in range(3):
            if not self.running:
                return
            self.append_text(loading_text[i % 3])
            time.sleep(0.8)

    def generate_fake_progress(self):
        for i in range(101):
            if not self.running:
                return
            self.progress["value"] = i
            self.root.update_idletasks()
            time.sleep(0.02 + random.uniform(0, 0.01))

    def run_fake_messages(self):
        while self.running:
            if random.random() < 0.05:
                self.show_both_popups("⚠️ Network instability detected!")

            message = self.get_random_message()
            timestamp = datetime.now().strftime("[%H:%M:%S] ")
            full_message = timestamp + message
            self.append_text(full_message)
            winsound.MessageBeep()

            if "backdoor" in message.lower():
                self.show_both_popups("⚠️ Backdoor detected!")
            elif random.random() < 0.1:
                self.show_both_popups(self.get_random_popup_message())

            time.sleep(random.uniform(0.3, 1.0))

    def append_text(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.write_log(text)

    def write_log(self, text):
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception as e:
            print(f"로그 저장 중 오류: {e}")

    def get_random_message(self):
        ip = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        port = random.randint(1, 65535)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        base_messages = [
            f"[*] Target found at {ip}",
            "[*] Scanning open ports...",
            f"[+] Port {port} open",
            "[*] Brute forcing password...",
            f"[+] Password found: {password}",
            "[*] Accessing system...",
            "[+] Downloading files...",
            "[*] Uploading malware...",
            "[+] Operation complete.",
            "[!] Connection lost.",
            "[*] Reestablishing connection...",
            "[+] Connected to secure shell",
            "[!] Firewall bypassed",
            "[+] Admin panel compromised",
            "[*] Exfiltrating data...",
            "[!] Backdoor installed successfully.",
        ]

        custom_messages = [
            "[!] D-DOS Confirmed.",
            "[+] D-DOS Complete.",
            f"[!] ERR 404 Target {ip} is No Found.",
            f"[!] Port {port} (HTTP) close.",
            f"[!] Port {port} (SSH) close",
            f"[+] Port {port} (HTTP) open",
            f"[+] Port {port} (SSH) open",
            "[!] Attack Failed: Attack Type: D-DOS Error Format: Defended",
            "[!] Attack Failed: Attack Type: Worm computer virus program(aaa.exe) Error Format: Defended(deleted File)"
        ]

        all_msgs = base_messages + custom_messages + self.custom_messages
        return random.choice(all_msgs)

    def get_random_popup_message(self):
        return random.choice([
            "⚠️ D-DOS 공격 감지됨!",
            "❌ 시스템 방화벽 활성화됨.",
            "🛑 접속 실패: 인증 오류",
            "🚫 악성코드 삭제됨",
            "💣 치명적 오류 발생. 로그 기록 중..."
        ])

    def show_both_popups(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.write_log(timestamp + message)

        popup = AutoClosePopup(self.root, message, duration=5000)
        popup.grab_set()

        if toaster:
            toaster.show_toast("Hacking_app", message, duration=3, threaded=True)

    def open_log_file(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.log_file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", self.log_file_path])
            else:
                subprocess.call(["xdg-open", self.log_file_path])
        except Exception as e:
            messagebox.showerror("Error", f"로그 파일 열기 실패: {e}")

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style(root)
    style.theme_use('default')
    style.configure("Dark.Horizontal.TProgressbar", troughcolor='black', background='lime')
    style.configure("Light.Horizontal.TProgressbar", troughcolor='white', background='green')

    app = FakeHackerGUI(root)
    app.apply_dark_theme()
    root.mainloop()
