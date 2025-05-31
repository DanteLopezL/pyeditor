import unittest
from unittest.mock import Mock, patch, mock_open
import tkinter as tk
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from gui.editor import FileEditor


class TestFileEditor(unittest.TestCase):
    def setUp(self):
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.winfo_children.return_value = []

        with patch("gui.editor.LoginWindow"):
            self.editor = FileEditor(self.mock_root)

        self.setup_ui_mocks()

    def setup_ui_mocks(self):
        self.mock_text_area = Mock()
        self.mock_text_area.get.return_value = ""
        self.mock_text_area.delete = Mock()
        self.mock_text_area.insert = Mock()

        self.mock_status_bar = Mock()

        self.mock_menu_bar = Mock()
        self.mock_file_menu = Mock()

        self.editor.text_area = self.mock_text_area
        self.editor.status_bar = self.mock_status_bar
        self.editor.menu_bar = self.mock_menu_bar
        self.editor.file_menu = self.mock_file_menu

    @patch("gui.editor.filedialog.askopenfilename")
    @patch("builtins.open", new_callable=mock_open, read_data="file content")
    def test_open_file_success(self, mock_file, mock_filedialog):
        self.editor.current_user = "test_user"
        mock_filedialog.return_value = "/path/to/file.txt"

        self.editor.open_file()

        mock_filedialog.assert_called_once()
        mock_file.assert_called_once_with("/path/to/file.txt", "r", encoding="utf-8")
        self.mock_text_area.delete.assert_called_with(1.0, tk.END)
        self.mock_text_area.insert.assert_called_with(tk.END, "file content")
        self.assertEqual(self.editor.current_file, "/path/to/file.txt")
        self.mock_status_bar.config.assert_called_with(
            text="Opened: /path/to/file.txt - Logged in as: test_user"
        )

    @patch("gui.editor.filedialog.asksaveasfilename")
    @patch.object(FileEditor, "save_file")
    def test_save_as_file_success(self, mock_save_file, mock_filedialog):
        mock_filedialog.return_value = "/path/to/newfile.txt"

        self.editor.save_as_file()

        mock_filedialog.assert_called_once()
        self.assertEqual(self.editor.current_file, "/path/to/newfile.txt")
        mock_save_file.assert_called_once()


if __name__ == "__main__":
    unittest.main()
