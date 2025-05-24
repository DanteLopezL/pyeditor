import tkinter as tk
import platform
import psutil


class AboutWindow:
    def __init__(self, master):
        self.master = master
        master.title("About System")

        # Get system info
        os_info = self.get_os_info()

        # Create and place label with OS info
        self.label = tk.Label(master, text=os_info, justify="left", padx=10, pady=10)
        self.label.pack()

    @staticmethod
    def get_os_info():
        os_name = platform.system()
        os_version = platform.version()
        processor = platform.processor()
        cpu_count = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024**3), 2)

        info = (
            f"Operating System: {os_name} {os_version}\n"
            f"Processor: {processor}\n"
            f"CPU Cores: {cpu_count}\n"
            f"RAM: {ram} GB"
        )
        return info
