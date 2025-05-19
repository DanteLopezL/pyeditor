import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import sqlite3
import hashlib


class Database:
    def __init__(self, db_name="file_editor.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None


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

        # Final lift to front
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


class FileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor - Please Login")
        self.root.geometry("800x600")

        # Mac-specific fixes for main window
        self.root.configure(bg="white")

        self.current_file = None
        self.current_user = None

        # Hide main window initially
        self.root.withdraw()

        # Show login window
        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, username):
        self.current_user = username
        self.root.title(f"File Editor - Welcome {username}")
        self.root.deiconify()

        # Bring main window to front after login
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)

        self.setup_ui()

    def setup_ui(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Account menu
        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="User Info", command=self.show_user_info)
        account_menu.add_command(label="Logout", command=self.logout)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)

        self.root.config(menu=self.menu_bar)

        # Text area with frame
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

        # Status bar
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
            # Clear the menu
            self.root.config(menu=tk.Menu(self.root))
            # Show login window again
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
                # Remove the extra newline that tkinter adds
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


def main():
    root = tk.Tk()

    # Mac-specific root window setup
    try:
        # Enable Mac-specific features if available
        root.createcommand("::tk::mac::ShowPreferences", lambda: None)
    except Exception as e:
        print(f"Failed due to {e}")

    FileEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
