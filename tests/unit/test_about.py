import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from gui.about import AboutWindow


class TestAboutWindow(unittest.TestCase):
    def setUp(self):
        self.mock_parent = Mock(spec=tk.Tk)

        with (
            patch("gui.about.tk.Frame") as mock_frame,
            patch("gui.about.tk.Label") as mock_label,
            patch("gui.about.tk.Button") as mock_button,
        ):
            self.mock_main_frame = Mock()
            mock_frame.return_value = self.mock_main_frame

            self.mock_prompt_label = Mock()
            self.mock_password_display = Mock()
            self.mock_enter_btn = Mock()
            self.mock_clear_btn = Mock()

            mock_label.side_effect = [
                self.mock_prompt_label,
                self.mock_password_display,
            ]
            mock_button.side_effect = [self.mock_enter_btn, self.mock_clear_btn]

            with patch.object(AboutWindow, "create_numeric_keyboard"):
                self.about_window = AboutWindow(self.mock_parent)

    def test_on_key_press_multiple_digits(self):
        self.about_window.on_key_press("1")
        self.about_window.on_key_press("7")
        self.about_window.on_key_press("0")
        self.about_window.on_key_press("5")

        self.assertEqual(self.about_window.entered_password, "1705")
        self.mock_password_display.config.assert_called_with(text="****")
        self.mock_enter_btn.config.assert_called_with(state=tk.NORMAL)

    def test_on_key_press_limits_to_four_digits(self):
        for digit in "12345":
            self.about_window.on_key_press(digit)

        self.assertEqual(self.about_window.entered_password, "1234")
        self.assertEqual(len(self.about_window.entered_password), 4)

    def test_clear_password_resets_state(self):
        self.about_window.entered_password = "123"

        self.about_window.clear_password()

        self.assertEqual(self.about_window.entered_password, "")
        self.mock_password_display.config.assert_called_with(text="")
        self.mock_enter_btn.config.assert_called_with(state=tk.DISABLED)

    def test_check_password_correct(self):
        self.about_window.entered_password = "1705"

        with patch.object(self.about_window, "show_system_info") as mock_show_info:
            self.about_window.check_password()

            mock_show_info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
