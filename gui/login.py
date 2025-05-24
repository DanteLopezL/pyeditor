from tkinter import messagebox
import tkinter as tk
from db.db import Database


class LoginWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.db = Database()
        self.create_login_window()

    def create_login_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Login - File Editor")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        # More aggressive Mac-specific fixes
        self.window.configure(bg="#f0f0f0")

        # Force immediate update before doing anything else
        self.window.update()

        # Multiple techniques to ensure visibility on Mac
        self.window.lift()
        self.window.focus_force()
        self.window.attributes("-topmost", True)

        # Set grab after window is properly configured
        self.window.grab_set()

        # Remove topmost after a delay
        self.window.after(500, lambda: self.window.attributes("-topmost", False))

        # Center the window with immediate effect
        self.center_window()

        # Force another update
        self.window.update_idletasks()

        # Create widgets immediately but with forced updates
        self.create_widgets()

    def center_window(self):
        # Force update before calculating positions
        self.window.update_idletasks()

        # Get actual screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate center position
        x = (screen_width - 400) // 2
        y = (screen_height - 350) // 2

        # Set geometry and force update
        self.window.geometry(f"400x350+{x}+{y}")
        self.window.update()

    def create_widgets(self):
        # Force immediate background color
        self.window.configure(bg="#f0f0f0")

        # Main container with explicit background
        main_frame = tk.Frame(self.window, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Force frame update
        main_frame.update()

        # Title with explicit styling
        title_label = tk.Label(
            main_frame,
            text="File Editor Login",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        title_label.pack(pady=(0, 20))

        # Form frame with background
        form_frame = tk.Frame(main_frame, bg="#f0f0f0")
        form_frame.pack()

        # Username section
        tk.Label(
            form_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0", fg="#333333"
        ).pack(pady=5, anchor=tk.W)
        self.username_entry = tk.Entry(
            form_frame, width=25, font=("Arial", 12), relief=tk.SOLID, bd=1
        )
        self.username_entry.pack(pady=5)

        # Password section
        tk.Label(
            form_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0", fg="#333333"
        ).pack(pady=5, anchor=tk.W)
        self.password_entry = tk.Entry(
            form_frame, width=25, show="*", font=("Arial", 12), relief=tk.SOLID, bd=1
        )
        self.password_entry.pack(pady=5)

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Buttons with explicit styling
        login_btn = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=10,
            relief=tk.RAISED,
            bd=2,
        )
        login_btn.pack(side=tk.LEFT, padx=5)

        register_btn = tk.Button(
            button_frame,
            text="Register",
            command=self.register,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=10,
            relief=tk.RAISED,
            bd=2,
        )
        register_btn.pack(side=tk.LEFT, padx=5)

        # Status label with background
        self.status_label = tk.Label(
            main_frame,
            text="Enter your credentials",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666",
        )
        self.status_label.pack(pady=10)

        # Instructions
        instructions = tk.Label(
            main_frame,
            text="New user? Click Register to create an account.",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#888888",
        )
        instructions.pack(pady=(10, 0))

        # Key bindings
        self.window.bind("<Return>", lambda e: self.login())
        self.window.bind("<Escape>", lambda e: self.window.quit())

        # Focus and final updates
        self.username_entry.focus_set()

        # Multiple forced updates to ensure rendering
        self.window.update()
        main_frame.update()
        self.window.update_idletasks()

        self.window.lift()
        self.window.focus_force()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(
                text="Please enter both username and password", fg="red"
            )
            return

        if self.db.authenticate_user(username, password):
            self.window.destroy()
            self.callback(username)
        else:
            self.status_label.config(text="Invalid username or password", fg="red")
            self.password_entry.delete(0, tk.END)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(
                text="Please enter both username and password", fg="red"
            )
            return

        if len(password) < 6:
            self.status_label.config(
                text="Password must be at least 6 characters", fg="red"
            )
            return

        if self.db.create_user(username, password):
            self.status_label.config(
                text="Registration successful! You can now login", fg="green"
            )
            messagebox.showinfo(
                "Success", "User registered successfully! You can now login."
            )
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
        else:
            self.status_label.config(text="Username already exists", fg="red")
