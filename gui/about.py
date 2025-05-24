import tkinter as tk
import platform
import psutil


class AboutWindow:
    def __init__(self, master):
        self.master = master
        master.title("System Information")
        master.geometry("500x500")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.version_label = tk.Label(
            self.main_frame,
            text="File Editor v1.0.0\nOpen Source Project",
            font=("Helvetica", 12, "bold"),
        )
        self.version_label.pack(pady=5)

        self.info_label = tk.Label(
            self.main_frame, text=self.get_os_info(), justify=tk.LEFT, anchor="w"
        )
        self.info_label.pack(fill=tk.X, pady=10)

        self.charts_frame = tk.Frame(self.main_frame)
        self.charts_frame.pack(fill=tk.BOTH, expand=True)

        self.ram_frame = tk.LabelFrame(self.charts_frame, text="RAM Usage")
        self.ram_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.ram_canvas = tk.Canvas(self.ram_frame, width=200, height=200, bg="white")
        self.ram_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.cpu_frame = tk.LabelFrame(self.charts_frame, text="CPU Usage")
        self.cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.cpu_canvas = tk.Canvas(self.cpu_frame, width=200, height=200, bg="white")
        self.cpu_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.update_btn = tk.Button(
            self.main_frame, text="Update", command=self.update_pie_charts
        )
        self.update_btn.pack(pady=10)

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
