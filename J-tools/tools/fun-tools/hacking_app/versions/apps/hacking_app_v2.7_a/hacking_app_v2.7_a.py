import tkinter as tk
import random
import time
import string
from threading import Thread
from tkinter import ttk
from datetime import datetime
import os

try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
except ImportError:
    toaster = None
    print("win10toast 라이브러리를 설치하면 윈도우 알림을 사용할 수 있습니다. (pip install win10toast)")

class AutoClosePopup(tk.Toplevel):
    def __init__(self, master, message, duration=3000):
        super().__init__(master)
        self.title("WARNING")
        self.configure(bg="yellow")
        self.resizable(False, False)

        label = tk.Label(self, text=message, bg="yellow", fg="red", font=("Arial", 12, "bold"))
        label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        popup_width = 300
        popup_height = 100
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
        self.root.title("Hacking Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(fill=tk.X)

        self.text_area = tk.Text(
            root,
            bg="black",
            fg="lime",
            insertbackground="lime",
            font=("Courier", 12),
            wrap=tk.WORD
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.config(state=tk.DISABLED)

        button_frame = tk.Frame(root, bg="black")
        button_frame.pack(pady=5)

        self.start_button = tk.Button(
            button_frame, text="Start Hacking", command=self.start_hacking, bg="green", fg="black"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(
            button_frame, text="Stop", command=self.stop_hacking, bg="red", fg="white"
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(
            button_frame, text="Clear (CLS)", command=self.clear_text, bg="gray", fg="white"
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.running = False

        # 로그 폴더 및 파일 경로 설정
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LOGS")
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file_path = os.path.join(self.log_dir, "hacking_simulator.log")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def start_hacking(self):
        if not self.running:
            self.running = True
            self.root.title("Hacking...")
            self.root.config(cursor="watch")   # 해킹 시작 시 'watch' 커서로 변경
            Thread(target=self.run_hacking_sequence, daemon=True).start()

    def stop_hacking(self):
        if self.running:
            self.running = False
            self.append_text("[SYSTEM] Hacking stopping...")
            self.root.title("Stopping...")
            self.root.config(cursor="arrow")    # 해킹 멈출 때 기본 커서로 변경
            time.sleep(0.5)
            self.root.title("Hacking_app_v2.7_a[bata]")
            self.progress['value'] = 0

    def clear_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)

    def run_hacking_sequence(self):
        self.simulate_loading()
        self.generate_fake_progress()
        self.run_fake_messages()

    def simulate_loading(self):
        loading_text = ["[.] Loading modules", "[..] Initializing network", "[...] Connecting..."]
        for i in range(3):
            if not self.running: return
            self.append_text(loading_text[i % 3])
            time.sleep(0.8)

    def generate_fake_progress(self):
        for i in range(101):
            if not self.running: return
            self.progress["value"] = i
            self.root.update_idletasks()
            time.sleep(0.02 + random.uniform(0, 0.01))

    def run_fake_messages(self):
        while self.running:
            message = self.get_random_message()
            timestamp = datetime.now().strftime("[%H:%M:%S] ")
            full_message = timestamp + message
            self.append_text(full_message)

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

        # 텍스트를 로그 파일에 기록
        self.write_log(text)

    def write_log(self, text):
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception as e:
            print(f"로그 저장 중 오류 발생: {e}")

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
            "[!] DANGER : D-DOS Confirmed.",
            "[+] D-DOS Complete.",
            f"[!] ERR 404 Target {ip} is No Found.",
            f"[!] Port {port} (HTTP) close.",
            f"[!] Port {port} (SSH) close",
            f"[+] Port {port} (HTTP) open",
            f"[+] Port {port} (SSH) open",
            "[!] Attack Failed: Attack Type: D-DOS Error Format: Defended",
            "[!] Attack Failed: Attack Type: Worm computer virus program(aaa.exe) Error Format: Defended(deleted File)"
        ]

        return random.choice(base_messages + custom_messages)

    def get_random_popup_message(self):
        return random.choice([
            "⚠️ D-DOS 공격 감지됨!",
            "❌ 시스템 방화벽 활성화됨.",
            "🛑 접속 실패: 인증 오류",
            "🚫 악성코드 삭제됨",
            "💣 치명적 오류 발생. 로그 기록 중..."
        ])

    def show_both_popups(self, message):
        # 팝업 뜰 때 로그에도 기록
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.write_log(timestamp + message)

        popup = AutoClosePopup(self.root, message, duration=3000)
        popup.grab_set()

        if toaster:
            toaster.show_toast("Hacking_app_v2.7_a[bata]", message, duration=3, threaded=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = FakeHackerGUI(root)
    root.mainloop()
