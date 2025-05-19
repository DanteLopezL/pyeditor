import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox


class FileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        self.root.geometry("800x600")
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        root.config(menu=self.menu_bar)

        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Consolas", 12),
            undo=True,
        )
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.status_bar = tk.Label(
            root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Rust/Python Files", "*.rs *.py"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.current_file = file_path
                    self.status_bar.config(text=f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        if not self.current_file:
            self.save_as_file()
            return

        try:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
                self.status_bar.config(text=f"Saved: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".rs",
            filetypes=[
                ("Rust Files", "*.rs"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ],
        )

        if file_path:
            self.current_file = file_path
            self.save_file()


def main():
    root = tk.Tk()
    FileEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
