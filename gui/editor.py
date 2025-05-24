from tkinter import scrolledtext, filedialog, messagebox
from gui.login import LoginWindow
import tkinter as tk


class FileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor - Please Login")
        self.root.geometry("800x600")

        self.root.configure(bg="white")

        self.current_file = None
        self.current_user = None

        self.root.withdraw()

        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, username):
        self.current_user = username
        self.root.title(f"File Editor - Welcome {username}")
        self.root.deiconify()

        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)

        self.setup_ui()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="User Info", command=self.show_user_info)
        account_menu.add_command(label="Logout", command=self.logout)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)

        self.root.config(menu=self.menu_bar)

        text_frame = tk.Frame(self.root)
        text_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Consolas", 12),
            undo=True,
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.status_bar = tk.Label(
            self.root,
            text=f"Ready - Logged in as: {self.current_user}",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        """Create a new file"""
        if self.text_area.get(1.0, tk.END).strip():
            if messagebox.askyesno(
                "New File", "Unsaved changes will be lost. Continue?"
            ):
                self.text_area.delete(1.0, tk.END)
                self.current_file = None
                self.status_bar.config(
                    text=f"New file - Logged in as: {self.current_user}"
                )
        else:
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.status_bar.config(text=f"New file - Logged in as: {self.current_user}")

    def show_user_info(self):
        info = f"Current User: {self.current_user}\nCurrent File: {self.current_file or 'None'}"
        messagebox.showinfo("User Information", info)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.withdraw()
            self.current_user = None
            self.current_file = None
            self.root.config(menu=tk.Menu(self.root))
            LoginWindow(self.root, self.on_login_success)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("Rust Files", "*.rs"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.current_file = file_path
                    self.status_bar.config(
                        text=f"Opened: {file_path} - Logged in as: {self.current_user}"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        if not self.current_file:
            self.save_as_file()
            return
        try:
            with open(self.current_file, "w", encoding="utf-8") as file:
                content = self.text_area.get(1.0, tk.END)
                if content.endswith("\n"):
                    content = content[:-1]
                file.write(content)
                self.status_bar.config(
                    text=f"Saved: {self.current_file} - Logged in as: {self.current_user}"
                )
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("Rust Files", "*.rs"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.current_file = file_path
            self.save_file()
