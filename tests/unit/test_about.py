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
        """Set up test fixtures with mocked tkinter components"""
        # Create a mock parent window
        self.mock_parent = Mock(spec=tk.Tk)

        # Mock all tkinter components to avoid actual GUI creation
        with patch("gui.about.tk.Frame") as mock_frame, \
             patch("gui.about.tk.Label") as mock_label, \
             patch("gui.about.tk.Button") as mock_button:

            # Set up mock returns
            self.mock_main_frame = Mock()
            mock_frame.return_value = self.mock_main_frame

            self.mock_prompt_label = Mock()
            self.mock_password_display = Mock()
            self.mock_enter_btn = Mock()
            self.mock_clear_btn = Mock()

            mock_label.side_effect = [
                self.mock_prompt_label,
                self.mock_password_display
            ]
            mock_button.side_effect = [
                self.mock_enter_btn,
                self.mock_clear_btn
            ]

            # Create AboutWindow instance
            with patch.object(AboutWindow, 'create_numeric_keyboard'):
                self.about_window = AboutWindow(self.mock_parent)



    def test_init_sets_correct_attributes(self):
        """Test that AboutWindow initializes with correct default values"""
        self.assertEqual(self.about_window.correct_password, "1705")
        self.assertEqual(self.about_window.entered_password, "")
        self.assertEqual(self.about_window.parent, self.mock_parent)

    def test_on_key_press_adds_digit(self):
        """Test that numeric key press adds digit to password"""
        self.about_window.on_key_press("1")

        self.assertEqual(self.about_window.entered_password, "1")
        self.mock_password_display.config.assert_called_with(text="*")
        self.mock_enter_btn.config.assert_called_with(state=tk.DISABLED)

    def test_on_key_press_multiple_digits(self):
        """Test that multiple key presses build up password"""
        self.about_window.on_key_press("1")
        self.about_window.on_key_press("7")
        self.about_window.on_key_press("0")
        self.about_window.on_key_press("5")

        self.assertEqual(self.about_window.entered_password, "1705")
        self.mock_password_display.config.assert_called_with(text="****")
        self.mock_enter_btn.config.assert_called_with(state=tk.NORMAL)

    def test_on_key_press_limits_to_four_digits(self):
        """Test that password is limited to 4 digits"""
        for digit in "12345":
            self.about_window.on_key_press(digit)

        self.assertEqual(self.about_window.entered_password, "1234")
        self.assertEqual(len(self.about_window.entered_password), 4)

    def test_on_key_press_backspace_removes_digit(self):
        """Test that backspace key removes last digit"""
        self.about_window.entered_password = "123"
        self.about_window.on_key_press("⌫")

        self.assertEqual(self.about_window.entered_password, "12")
        self.mock_password_display.config.assert_called_with(text="**")
        self.mock_enter_btn.config.assert_called_with(state=tk.DISABLED)

    def test_on_key_press_backspace_on_empty_password(self):
        """Test that backspace on empty password doesn't cause errors"""
        self.about_window.entered_password = ""
        self.about_window.on_key_press("⌫")

        self.assertEqual(self.about_window.entered_password, "")
        self.mock_password_display.config.assert_called_with(text="")

    def test_clear_password_resets_state(self):
        """Test that clear password resets all password-related state"""
        self.about_window.entered_password = "123"

        self.about_window.clear_password()

        self.assertEqual(self.about_window.entered_password, "")
        self.mock_password_display.config.assert_called_with(text="")
        self.mock_enter_btn.config.assert_called_with(state=tk.DISABLED)

    @patch("gui.about.messagebox.showerror")
    def test_check_password_incorrect(self, mock_showerror):
        """Test password check with incorrect password"""
        self.about_window.entered_password = "1234"

        with patch.object(self.about_window, 'clear_password') as mock_clear:
            self.about_window.check_password()

            mock_showerror.assert_called_with("Access Denied", "Incorrect PIN")
            mock_clear.assert_called_once()

    def test_check_password_correct(self):
        """Test password check with correct password"""
        self.about_window.entered_password = "1705"

        with patch.object(self.about_window, 'show_system_info') as mock_show_info:
            self.about_window.check_password()

            mock_show_info.assert_called_once()

    @patch("gui.about.tk.Frame")
    @patch("gui.about.tk.Label")
    @patch("gui.about.tk.Button")
    @patch("gui.about.tk.LabelFrame")
    @patch("gui.about.tk.Canvas")
    def test_show_system_info_creates_ui_components(
        self, mock_canvas, mock_labelframe, mock_button, mock_label, mock_frame
    ):
        """Test that show_system_info creates all necessary UI components"""
        # Mock the main frame's children
        mock_child1 = Mock()
        mock_child2 = Mock()
        self.mock_main_frame.winfo_children.return_value = [mock_child1, mock_child2]

        # Mock canvas instances
        mock_ram_canvas = Mock()
        mock_cpu_canvas = Mock()
        mock_canvas.side_effect = [mock_ram_canvas, mock_cpu_canvas]

        with patch.object(self.about_window, 'get_os_info') as mock_get_os_info, \
             patch.object(self.about_window, 'update_pie_charts') as mock_update_charts:

            mock_get_os_info.return_value = "Mock OS Info"

            self.about_window.show_system_info()

            # Verify old widgets are destroyed
            mock_child1.destroy.assert_called_once()
            mock_child2.destroy.assert_called_once()

            # Verify parent title is updated
            self.mock_parent.title.assert_called_with("System Information")

            # Verify UI components are created
            self.assertTrue(mock_label.called)
            self.assertTrue(mock_labelframe.called)
            self.assertTrue(mock_canvas.called)
            self.assertTrue(mock_button.called)

            # Verify canvas instances are stored
            self.assertEqual(self.about_window.ram_canvas, mock_ram_canvas)
            self.assertEqual(self.about_window.cpu_canvas, mock_cpu_canvas)

            # Verify charts are updated
            mock_update_charts.assert_called_once()

    @patch("gui.about.platform.system")
    @patch("gui.about.platform.version")
    @patch("gui.about.platform.processor")
    @patch("gui.about.psutil.cpu_count")
    @patch("gui.about.psutil.virtual_memory")
    def test_get_os_info_returns_formatted_string(
        self, mock_virtual_memory, mock_cpu_count, mock_processor, mock_version, mock_system
    ):
        """Test that get_os_info returns properly formatted system information"""
        # Mock system information
        mock_system.return_value = "Linux"
        mock_version.return_value = "5.4.0"
        mock_processor.return_value = "x86_64"
        mock_cpu_count.return_value = 8

        mock_memory = Mock()
        mock_memory.total = 16 * (1024**3)  # 16 GB in bytes
        mock_virtual_memory.return_value = mock_memory

        result = AboutWindow.get_os_info()

        expected = (
            "OS: Linux 5.4.0\n"
            "Processor: x86_64\n"
            "CPU Cores: 8\n"
            "Total RAM: 16.0 GB"
        )

        self.assertEqual(result, expected)

    def test_draw_pie_chart_deletes_existing_content(self):
        """Test that draw_pie_chart clears existing canvas content"""
        mock_canvas = Mock()
        mock_canvas.winfo_width.return_value = 200
        mock_canvas.winfo_height.return_value = 200

        self.about_window.draw_pie_chart(mock_canvas, 50, "Test Chart")

        mock_canvas.delete.assert_called_with("all")

    def test_draw_pie_chart_creates_visual_elements(self):
        """Test that draw_pie_chart creates all necessary visual elements"""
        mock_canvas = Mock()
        mock_canvas.winfo_width.return_value = 200
        mock_canvas.winfo_height.return_value = 200

        self.about_window.draw_pie_chart(mock_canvas, 75, "Test Chart")

        # Verify canvas drawing methods are called
        self.assertEqual(mock_canvas.create_arc.call_count, 2)  # Used and free portions
        mock_canvas.create_oval.assert_called_once()  # Inner circle
        self.assertEqual(mock_canvas.create_text.call_count, 2)  # Percentage and title

    def test_draw_pie_chart_calculates_correct_angles(self):
        """Test that draw_pie_chart calculates correct angles for pie slices"""
        mock_canvas = Mock()
        mock_canvas.winfo_width.return_value = 200
        mock_canvas.winfo_height.return_value = 200

        self.about_window.draw_pie_chart(mock_canvas, 25, "Test Chart")

        # Check that the angles are calculated correctly (25% = 90 degrees)
        calls = mock_canvas.create_arc.call_args_list

        # First arc (used portion)
        used_call = calls[0]
        self.assertEqual(used_call[1]['start'], 0)
        self.assertEqual(used_call[1]['extent'], 90)  # 25% of 360

        # Second arc (free portion)
        free_call = calls[1]
        self.assertEqual(free_call[1]['start'], 90)
        self.assertEqual(free_call[1]['extent'], 270)  # 75% of 360

    @patch("gui.about.psutil.virtual_memory")
    @patch("gui.about.psutil.cpu_percent")
    def test_update_pie_charts_updates_both_charts(self, mock_cpu_percent, mock_virtual_memory):
        """Test that update_pie_charts updates both RAM and CPU charts"""
        # Mock system data
        mock_memory = Mock()
        mock_memory.percent = 60.5
        mock_memory.used = 8 * (1024**3)  # 8 GB
        mock_memory.total = 16 * (1024**3)  # 16 GB
        mock_virtual_memory.return_value = mock_memory

        mock_cpu_percent.return_value = 45.2

        # Mock canvas objects
        self.about_window.ram_canvas = Mock()
        self.about_window.cpu_canvas = Mock()

        with patch.object(self.about_window, 'draw_pie_chart') as mock_draw:
            self.about_window.update_pie_charts()

            # Verify both charts are drawn
            self.assertEqual(mock_draw.call_count, 2)

            # Check RAM chart call
            ram_call = mock_draw.call_args_list[0]
            self.assertEqual(ram_call[0][0], self.about_window.ram_canvas)
            self.assertEqual(ram_call[0][1], 60.5)
            self.assertIn("RAM:", ram_call[0][2])

            # Check CPU chart call
            cpu_call = mock_draw.call_args_list[1]
            self.assertEqual(cpu_call[0][0], self.about_window.cpu_canvas)
            self.assertEqual(cpu_call[0][1], 45.2)
            self.assertEqual(cpu_call[0][2], "CPU Usage")



if __name__ == "__main__":
    unittest.main()
