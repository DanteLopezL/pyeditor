import tkinter as tk
from gui.editor import FileEditor


def main():
    root = tk.Tk()

    FileEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
