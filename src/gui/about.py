import tkinter as tk
from tkinter import messagebox
import platform
import psutil


class AboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Authentication Required")
        self.parent.geometry("400x500")

        self.correct_password = "1705"
        self.entered_password = ""

        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.prompt_label = tk.Label(
            self.main_frame,
            text="Enter PIN to view system information:",
            font=("Helvetica", 12),
        )
        self.prompt_label.pack(pady=10)

        self.password_display = tk.Label(
            self.main_frame, text="", font=("Helvetica", 24), width=10, relief=tk.SUNKEN
        )
        self.password_display.pack(pady=10)

        self.create_numeric_keyboard()

        self.enter_btn = tk.Button(
            self.main_frame,
            text="ENTER",
            font=("Helvetica", 12, "bold"),
            command=self.check_password,
            state=tk.DISABLED,
        )
        self.enter_btn.pack(pady=10, fill=tk.X)

        self.clear_btn = tk.Button(
            self.main_frame,
            text="CLEAR",
            font=("Helvetica", 10),
            command=self.clear_password,
        )
        self.clear_btn.pack(fill=tk.X)

    def create_numeric_keyboard(self):
        buttons = [
            ("1", "2", "3"),
            ("4", "5", "6"),
            ("7", "8", "9"),
            ("", "0", "⌫"),
        ]

        for row in buttons:
            frame = tk.Frame(self.main_frame)
            frame.pack(fill=tk.X)
            for key in row:
                if key == "":
                    tk.Label(frame, width=5).pack(side=tk.LEFT, expand=True)
                else:
                    btn = tk.Button(
                        frame,
                        text=key,
                        font=("Helvetica", 14),
                        width=5,
                        height=2,
                        command=lambda k=key: self.on_key_press(k),
                    )
                    btn.pack(side=tk.LEFT, expand=True, padx=2, pady=2)

    def on_key_press(self, key):
        if key == "⌫":
            self.entered_password = self.entered_password[:-1]
        elif len(self.entered_password) < 4:
            self.entered_password += key

        self.password_display.config(text="*" * len(self.entered_password))

        self.enter_btn.config(
            state=tk.NORMAL if len(self.entered_password) == 4 else tk.DISABLED
        )

    def clear_password(self):
        self.entered_password = ""
        self.password_display.config(text="")
        self.enter_btn.config(state=tk.DISABLED)

    def check_password(self):
        if self.entered_password == self.correct_password:
            self.show_system_info()
        else:
            messagebox.showerror("Access Denied", "Incorrect PIN")
            self.clear_password()

    def show_system_info(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.parent.title("System Information")

        tk.Label(
            self.main_frame,
            text="File Editor v1.0.0\nOpen Source Project",
            font=("Helvetica", 12, "bold"),
        ).pack(pady=5)

        tk.Label(
            self.main_frame, text=self.get_os_info(), justify=tk.LEFT, anchor="w"
        ).pack(fill=tk.X, pady=10)

        charts_frame = tk.Frame(self.main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True)

        ram_frame = tk.LabelFrame(charts_frame, text="RAM Usage")
        ram_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.ram_canvas = tk.Canvas(ram_frame, width=150, height=150, bg="white")
        self.ram_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cpu_frame = tk.LabelFrame(charts_frame, text="CPU Usage")
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.cpu_canvas = tk.Canvas(cpu_frame, width=150, height=150, bg="white")
        self.cpu_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Button(self.main_frame, text="Refresh", command=self.update_pie_charts).pack(
            pady=10
        )

        tk.Button(self.main_frame, text="Close", command=self.parent.destroy).pack(
            pady=5
        )

        self.update_pie_charts()

    @staticmethod
    def get_os_info():
        os_name = platform.system()
        os_version = platform.version()
        processor = platform.processor()
        cpu_count = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024**3), 2)

        info = (
            f"OS: {os_name} {os_version}\n"
            f"Processor: {processor}\n"
            f"CPU Cores: {cpu_count}\n"
            f"Total RAM: {ram} GB"
        )
        return info

    def draw_pie_chart(self, canvas, percent_used, title):
        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        radius = min(width, height) * 0.4
        center_x = width // 2
        center_y = height // 2

        used_color = "#ff9999"
        free_color = "#66b3ff"
        text_color = "black"

        used_angle = 360 * percent_used / 100
        free_angle = 360 - used_angle

        canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=0,
            extent=used_angle,
            fill=used_color,
            outline="white",
        )

        canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=used_angle,
            extent=free_angle,
            fill=free_color,
            outline="white",
        )

        inner_radius = radius * 0.5
        canvas.create_oval(
            center_x - inner_radius,
            center_y - inner_radius,
            center_x + inner_radius,
            center_y + inner_radius,
            fill="white",
            outline="white",
        )

        canvas.create_text(
            center_x,
            center_y,
            text=f"{percent_used:.1f}%",
            font=("Helvetica", 14, "bold"),
            fill=text_color,
        )

        canvas.create_text(
            center_x, height - 15, text=title, font=("Helvetica", 10), fill=text_color
        )

    def update_pie_charts(self):
        ram = psutil.virtual_memory()
        ram_used_percent = ram.percent
        self.draw_pie_chart(
            self.ram_canvas,
            ram_used_percent,
            f"RAM: {ram.used / (1024**3):.1f}/{ram.total / (1024**3):.1f} GB",
        )

        cpu_percent = psutil.cpu_percent(interval=1)
        self.draw_pie_chart(self.cpu_canvas, cpu_percent, "CPU Usage")


if __name__ == "__main__":
    root = tk.Tk()
    app = AboutWindow(root)
    root.mainloop()
