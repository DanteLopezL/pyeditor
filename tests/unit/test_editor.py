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
        """Set up test fixtures with mocked tkinter components"""
        # Create a mock root window
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.winfo_children.return_value = []

        # Mock the LoginWindow to avoid actual GUI creation
        with patch("gui.editor.LoginWindow") as mock_login:
            self.editor = FileEditor(self.mock_root)

        # Set up common mocks for UI components
        self.setup_ui_mocks()

    def setup_ui_mocks(self):
        """Set up mocks for UI components that are created in setup_ui"""
        # Mock text area
        self.mock_text_area = Mock()
        self.mock_text_area.get.return_value = ""
        self.mock_text_area.delete = Mock()
        self.mock_text_area.insert = Mock()

        # Mock status bar
        self.mock_status_bar = Mock()

        # Mock menu components
        self.mock_menu_bar = Mock()
        self.mock_file_menu = Mock()

        # Assign mocks to editor instance
        self.editor.text_area = self.mock_text_area
        self.editor.status_bar = self.mock_status_bar
        self.editor.menu_bar = self.mock_menu_bar
        self.editor.file_menu = self.mock_file_menu

    @patch("gui.editor.filedialog.askopenfilename")
    @patch("builtins.open", new_callable=mock_open, read_data="file content")
    def test_open_file_success(self, mock_file, mock_filedialog):
        """Test successful file opening"""
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

    @patch("gui.editor.filedialog.askopenfilename")
    def test_open_file_user_cancels(self, mock_filedialog):
        """Test file opening when user cancels dialog"""
        mock_filedialog.return_value = ""

        self.editor.open_file()

        mock_filedialog.assert_called_once()
        self.mock_text_area.delete.assert_not_called()
        self.mock_text_area.insert.assert_not_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("gui.editor.messagebox.showinfo")
    def test_save_file_with_existing_file(self, mock_messagebox, mock_file):
        """Test saving to an existing file"""
        self.editor.current_user = "test_user"
        self.editor.current_file = "/path/to/file.txt"
        self.mock_text_area.get.return_value = "file content\n"

        self.editor.save_file()

        mock_file.assert_called_once_with("/path/to/file.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("file content")
        mock_messagebox.assert_called_with("Success", "File saved successfully!")
        self.mock_status_bar.config.assert_called_with(
            text="Saved: /path/to/file.txt - Logged in as: test_user"
        )

    @patch("gui.editor.filedialog.asksaveasfilename")
    @patch.object(FileEditor, "save_file")
    def test_save_as_file_success(self, mock_save_file, mock_filedialog):
        """Test save as functionality"""
        mock_filedialog.return_value = "/path/to/newfile.txt"

        self.editor.save_as_file()

        mock_filedialog.assert_called_once()
        self.assertEqual(self.editor.current_file, "/path/to/newfile.txt")
        mock_save_file.assert_called_once()


if __name__ == "__main__":
    unittest.main()
