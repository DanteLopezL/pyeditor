import tkinter as tk
from gui.editor import FileEditor


def main():
    root = tk.Tk()

    try:
        root.createcommand("::tk::mac::ShowPreferences", lambda: None)
    except Exception as e:
        print(f"Failed due to {e}")

    FileEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
