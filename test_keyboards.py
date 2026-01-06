"""
Comprehensive test suite for the keyboards module.

This module contains unit tests for keyboard-related functionality including:
- Keyboard initialization and configuration
- Keyboard layout detection and switching
- Key press/release simulation
- Macro recording and playback
- Keyboard connectivity and status
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import pytest
from keyboards import (
    Keyboard,
    KeyboardLayout,
    KeyboardStatus,
    KeyboardError,
    MacroRecorder,
    KeyEvent,
)


class TestKeyEvent(unittest.TestCase):
    """Test cases for KeyEvent class."""

    def test_key_event_creation(self):
        """Test creating a KeyEvent with valid parameters."""
        event = KeyEvent(key='a', pressed=True)
        self.assertEqual(event.key, 'a')
        self.assertTrue(event.pressed)

    def test_key_event_with_timestamp(self):
        """Test KeyEvent with timestamp."""
        import time
        ts = time.time()
        event = KeyEvent(key='Enter', pressed=False, timestamp=ts)
        self.assertEqual(event.key, 'Enter')
        self.assertFalse(event.pressed)
        self.assertEqual(event.timestamp, ts)

    def test_key_event_repr(self):
        """Test string representation of KeyEvent."""
        event = KeyEvent(key='Space', pressed=True)
        repr_str = repr(event)
        self.assertIn('Space', repr_str)
        self.assertIn('pressed', repr_str.lower())

    def test_key_event_special_keys(self):
        """Test KeyEvent with special keys."""
        special_keys = ['Shift', 'Control', 'Alt', 'Meta', 'Enter', 'Tab', 'Escape']
        for key in special_keys:
            event = KeyEvent(key=key, pressed=True)
            self.assertEqual(event.key, key)


class TestKeyboardLayout(unittest.TestCase):
    """Test cases for KeyboardLayout class."""

    def test_default_layout(self):
        """Test default keyboard layout initialization."""
        layout = KeyboardLayout('QWERTY')
        self.assertEqual(layout.name, 'QWERTY')

    def test_layout_mapping(self):
        """Test keyboard layout character mapping."""
        layout = KeyboardLayout('QWERTY')
        self.assertIsNotNone(layout.get_mapping('a'))

    def test_switch_layout(self):
        """Test switching between keyboard layouts."""
        layout1 = KeyboardLayout('QWERTY')
        layout2 = KeyboardLayout('DVORAK')
        self.assertNotEqual(layout1.name, layout2.name)

    def test_layout_with_custom_mapping(self):
        """Test creating layout with custom mapping."""
        custom_map = {'a': '1', 'b': '2'}
        layout = KeyboardLayout('CUSTOM', mapping=custom_map)
        self.assertEqual(layout.get_mapping('a'), '1')
        self.assertEqual(layout.get_mapping('b'), '2')

    def test_supported_layouts(self):
        """Test checking available keyboard layouts."""
        supported = KeyboardLayout.get_supported_layouts()
        self.assertGreater(len(supported), 0)
        self.assertIn('QWERTY', supported)

    def test_invalid_layout(self):
        """Test handling of invalid layout."""
        with self.assertRaises(KeyboardError):
            KeyboardLayout('INVALID_LAYOUT_XYZ')


class TestKeyboardStatus(unittest.TestCase):
    """Test cases for KeyboardStatus enum."""

    def test_status_values(self):
        """Test KeyboardStatus enum values."""
        self.assertTrue(hasattr(KeyboardStatus, 'CONNECTED'))
        self.assertTrue(hasattr(KeyboardStatus, 'DISCONNECTED'))
        self.assertTrue(hasattr(KeyboardStatus, 'ERROR'))

    def test_status_comparison(self):
        """Test comparing KeyboardStatus values."""
        status1 = KeyboardStatus.CONNECTED
        status2 = KeyboardStatus.CONNECTED
        self.assertEqual(status1, status2)
        self.assertNotEqual(status1, KeyboardStatus.DISCONNECTED)


class TestKeyboard(unittest.TestCase):
    """Test cases for Keyboard class."""

    def setUp(self):
        """Set up test fixtures."""
        self.keyboard = Keyboard(device_id='keyboard_001')

    def test_keyboard_initialization(self):
        """Test keyboard initialization."""
        keyboard = Keyboard(device_id='test_keyboard')
        self.assertEqual(keyboard.device_id, 'test_keyboard')
        self.assertIsNotNone(keyboard.status)

    def test_keyboard_with_layout(self):
        """Test keyboard initialization with specific layout."""
        keyboard = Keyboard(device_id='test_kb', layout='DVORAK')
        self.assertEqual(keyboard.layout.name, 'DVORAK')

    def test_connect_keyboard(self):
        """Test connecting a keyboard."""
        with patch.object(self.keyboard, '_connect') as mock_connect:
            self.keyboard.connect()
            mock_connect.assert_called_once()

    def test_disconnect_keyboard(self):
        """Test disconnecting a keyboard."""
        with patch.object(self.keyboard, '_disconnect') as mock_disconnect:
            self.keyboard.disconnect()
            mock_disconnect.assert_called_once()

    def test_get_keyboard_info(self):
        """Test retrieving keyboard information."""
        info = self.keyboard.get_info()
        self.assertIsNotNone(info)
        self.assertIn('device_id', info)

    def test_get_keyboard_status(self):
        """Test retrieving keyboard status."""
        status = self.keyboard.get_status()
        self.assertIsNotNone(status)

    def test_press_key(self):
        """Test pressing a key."""
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.press_key('a')
            mock_send.assert_called_once()

    def test_release_key(self):
        """Test releasing a key."""
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.release_key('a')
            mock_send.assert_called_once()

    def test_type_string(self):
        """Test typing a string of characters."""
        with patch.object(self.keyboard, 'press_key') as mock_press:
            with patch.object(self.keyboard, 'release_key') as mock_release:
                self.keyboard.type_string('hello')
                self.assertEqual(mock_press.call_count, 5)
                self.assertEqual(mock_release.call_count, 5)

    def test_key_combination(self):
        """Test pressing key combinations."""
        with patch.object(self.keyboard, 'press_key') as mock_press:
            with patch.object(self.keyboard, 'release_key') as mock_release:
                self.keyboard.key_combination('Control', 'c')
                self.assertEqual(mock_press.call_count, 2)
                self.assertEqual(mock_release.call_count, 2)

    def test_set_layout(self):
        """Test changing keyboard layout."""
        original_layout = self.keyboard.layout.name
        self.keyboard.set_layout('DVORAK')
        self.assertEqual(self.keyboard.layout.name, 'DVORAK')
        self.assertNotEqual(self.keyboard.layout.name, original_layout)

    def test_set_invalid_layout(self):
        """Test setting invalid keyboard layout."""
        with self.assertRaises(KeyboardError):
            self.keyboard.set_layout('NONEXISTENT')

    def test_is_connected(self):
        """Test checking keyboard connection status."""
        is_connected = self.keyboard.is_connected()
        self.assertIsInstance(is_connected, bool)

    def test_keyboard_with_multiple_features(self):
        """Test keyboard with multiple features enabled."""
        keyboard = Keyboard(
            device_id='feature_kb',
            rgb_enabled=True,
            macro_enabled=True
        )
        self.assertTrue(keyboard.rgb_enabled)
        self.assertTrue(keyboard.macro_enabled)

    def test_get_keyboard_properties(self):
        """Test retrieving keyboard properties."""
        props = self.keyboard.get_properties()
        self.assertIsInstance(props, dict)
        if len(props) > 0:
            self.assertIn('device_id', props)

    def test_set_keyboard_property(self):
        """Test setting keyboard properties."""
        with patch.object(self.keyboard, '_set_property') as mock_set:
            self.keyboard.set_property('brightness', 50)
            mock_set.assert_called_once_with('brightness', 50)


class TestKeyboardInput(unittest.TestCase):
    """Test cases for keyboard input operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.keyboard = Keyboard(device_id='input_test_kb')

    def test_press_and_release_sequence(self):
        """Test sequence of press and release operations."""
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.press_key('Shift')
            self.keyboard.press_key('a')
            self.keyboard.release_key('a')
            self.keyboard.release_key('Shift')
            self.assertEqual(mock_send.call_count, 4)

    def test_type_with_special_characters(self):
        """Test typing strings with special characters."""
        special_string = "Hello! @#$%"
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.type_string(special_string)
            self.assertGreater(mock_send.call_count, 0)

    def test_rapid_keypresses(self):
        """Test rapid key press simulation."""
        with patch.object(self.keyboard, 'press_key') as mock_press:
            for i in range(10):
                self.keyboard.press_key('a')
            self.assertEqual(mock_press.call_count, 10)

    def test_key_held_duration(self):
        """Test holding a key for specific duration."""
        with patch('time.sleep') as mock_sleep:
            self.keyboard.hold_key('a', duration=1.0)
            mock_sleep.assert_called()

    def test_mouse_button_not_on_keyboard(self):
        """Test that mouse buttons cannot be pressed on keyboard."""
        with self.assertRaises(KeyboardError):
            self.keyboard.press_key('MouseButton1')


class TestMacroRecorder(unittest.TestCase):
    """Test cases for MacroRecorder class."""

    def setUp(self):
        """Set up test fixtures."""
        self.recorder = MacroRecorder()

    def test_recorder_initialization(self):
        """Test macro recorder initialization."""
        self.assertFalse(self.recorder.is_recording())

    def test_start_recording(self):
        """Test starting macro recording."""
        self.recorder.start_recording()
        self.assertTrue(self.recorder.is_recording())

    def test_stop_recording(self):
        """Test stopping macro recording."""
        self.recorder.start_recording()
        self.recorder.stop_recording()
        self.assertFalse(self.recorder.is_recording())

    def test_record_key_event(self):
        """Test recording key events."""
        self.recorder.start_recording()
        event1 = KeyEvent(key='a', pressed=True)
        event2 = KeyEvent(key='a', pressed=False)
        self.recorder.record_event(event1)
        self.recorder.record_event(event2)
        self.recorder.stop_recording()
        
        events = self.recorder.get_recorded_events()
        self.assertEqual(len(events), 2)

    def test_playback_macro(self):
        """Test playing back recorded macro."""
        self.recorder.start_recording()
        self.recorder.record_event(KeyEvent(key='a', pressed=True))
        self.recorder.record_event(KeyEvent(key='a', pressed=False))
        self.recorder.stop_recording()
        
        macro = self.recorder.get_macro()
        self.assertIsNotNone(macro)
        self.assertGreater(len(macro), 0)

    def test_save_macro(self):
        """Test saving macro to file."""
        self.recorder.start_recording()
        self.recorder.record_event(KeyEvent(key='b', pressed=True))
        self.recorder.record_event(KeyEvent(key='b', pressed=False))
        self.recorder.stop_recording()
        
        with patch.object(self.recorder, '_write_to_file') as mock_write:
            self.recorder.save_macro('test_macro.kbd')
            mock_write.assert_called_once()

    def test_load_macro(self):
        """Test loading macro from file."""
        with patch.object(self.recorder, '_read_from_file') as mock_read:
            mock_read.return_value = [
                KeyEvent(key='c', pressed=True),
                KeyEvent(key='c', pressed=False)
            ]
            macro = self.recorder.load_macro('test_macro.kbd')
            self.assertEqual(len(macro), 2)

    def test_clear_recorded_events(self):
        """Test clearing recorded events."""
        self.recorder.start_recording()
        self.recorder.record_event(KeyEvent(key='a', pressed=True))
        self.recorder.stop_recording()
        
        self.recorder.clear()
        events = self.recorder.get_recorded_events()
        self.assertEqual(len(events), 0)

    def test_get_recording_duration(self):
        """Test getting recording duration."""
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 5]  # 5 second duration
            self.recorder.start_recording()
            self.recorder.stop_recording()
            duration = self.recorder.get_duration()
            self.assertEqual(duration, 5)

    def test_macro_with_delays(self):
        """Test recording macro with delays between events."""
        self.recorder.start_recording()
        self.recorder.record_event(KeyEvent(key='a', pressed=True))
        self.recorder.add_delay(0.5)
        self.recorder.record_event(KeyEvent(key='a', pressed=False))
        self.recorder.stop_recording()
        
        macro = self.recorder.get_macro()
        self.assertGreaterEqual(len(macro), 2)


class TestKeyboardError(unittest.TestCase):
    """Test cases for KeyboardError exception."""

    def test_keyboard_error_creation(self):
        """Test creating a KeyboardError."""
        error = KeyboardError("Test error message")
        self.assertEqual(str(error), "Test error message")

    def test_keyboard_error_is_exception(self):
        """Test that KeyboardError is an Exception."""
        error = KeyboardError("Test")
        self.assertIsInstance(error, Exception)

    def test_raise_keyboard_error(self):
        """Test raising KeyboardError."""
        with self.assertRaises(KeyboardError):
            raise KeyboardError("Device not found")

    def test_keyboard_error_with_device_info(self):
        """Test KeyboardError with device information."""
        error = KeyboardError("Device error for device_001")
        self.assertIn("device_001", str(error))


class TestKeyboardIntegration(unittest.TestCase):
    """Integration tests for keyboard functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.keyboard = Keyboard(device_id='integration_kb')
        self.recorder = MacroRecorder()

    def test_record_and_playback_workflow(self):
        """Test complete workflow of recording and playback."""
        # Record a simple macro
        self.recorder.start_recording()
        self.recorder.record_event(KeyEvent(key='h', pressed=True))
        self.recorder.record_event(KeyEvent(key='h', pressed=False))
        self.recorder.record_event(KeyEvent(key='i', pressed=True))
        self.recorder.record_event(KeyEvent(key='i', pressed=False))
        self.recorder.stop_recording()
        
        # Verify recording
        events = self.recorder.get_recorded_events()
        self.assertEqual(len(events), 4)

    def test_keyboard_layout_switching_with_typing(self):
        """Test switching layouts and typing."""
        self.keyboard.set_layout('QWERTY')
        with patch.object(self.keyboard, 'type_string') as mock_type:
            self.keyboard.type_string('hello')
            mock_type.assert_called_once_with('hello')
        
        self.keyboard.set_layout('DVORAK')
        with patch.object(self.keyboard, 'type_string') as mock_type:
            self.keyboard.type_string('hello')
            mock_type.assert_called_once_with('hello')

    def test_multiple_keyboard_instances(self):
        """Test managing multiple keyboard instances."""
        kb1 = Keyboard(device_id='kb_001')
        kb2 = Keyboard(device_id='kb_002')
        
        self.assertNotEqual(kb1.device_id, kb2.device_id)
        
        with patch.object(kb1, 'press_key') as mock_press1:
            with patch.object(kb2, 'press_key') as mock_press2:
                kb1.press_key('a')
                kb2.press_key('b')
                mock_press1.assert_called_once_with('a')
                mock_press2.assert_called_once_with('b')

    def test_keyboard_with_recorder_integration(self):
        """Test keyboard integrated with macro recorder."""
        # Record keyboard events
        self.recorder.start_recording()
        
        event = KeyEvent(key='x', pressed=True)
        self.recorder.record_event(event)
        
        event = KeyEvent(key='x', pressed=False)
        self.recorder.record_event(event)
        
        self.recorder.stop_recording()
        
        # Verify macro was recorded
        macro = self.recorder.get_macro()
        self.assertIsNotNone(macro)
        self.assertEqual(len(macro), 2)


class TestKeyboardEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.keyboard = Keyboard(device_id='edge_case_kb')

    def test_empty_string_typing(self):
        """Test typing an empty string."""
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.type_string('')
            self.assertEqual(mock_send.call_count, 0)

    def test_very_long_string(self):
        """Test typing a very long string."""
        long_string = 'a' * 1000
        with patch.object(self.keyboard, '_send_key_event') as mock_send:
            self.keyboard.type_string(long_string)
            self.assertGreater(mock_send.call_count, 0)

    def test_unicode_characters(self):
        """Test typing unicode characters."""
        unicode_string = "Hello 世界 🎹"
        with patch.object(self.keyboard, 'type_string') as mock_type:
            self.keyboard.type_string(unicode_string)
            mock_type.assert_called_once_with(unicode_string)

    def test_rapid_connect_disconnect(self):
        """Test rapid connect/disconnect cycles."""
        with patch.object(self.keyboard, '_connect'):
            with patch.object(self.keyboard, '_disconnect'):
                for _ in range(5):
                    self.keyboard.connect()
                    self.keyboard.disconnect()

    def test_key_press_without_release(self):
        """Test pressing key without explicit release."""
        with patch.object(self.keyboard, '_send_key_event'):
            self.keyboard.press_key('Control')
            # Key remains pressed until release is called

    def test_macro_recorder_clear_during_recording(self):
        """Test clearing macro while recording."""
        recorder = MacroRecorder()
        recorder.start_recording()
        recorder.record_event(KeyEvent(key='a', pressed=True))
        recorder.clear()  # Clear while recording
        recorder.stop_recording()
        
        # After clearing, events should be cleared
        events = recorder.get_recorded_events()
        self.assertEqual(len(events), 0)


class TestKeyboardPerformance(unittest.TestCase):
    """Performance-related tests."""

    def test_keyboard_initialization_performance(self):
        """Test keyboard initialization doesn't block significantly."""
        import time
        start = time.time()
        keyboard = Keyboard(device_id='perf_test_kb')
        end = time.time()
        # Should initialize in reasonable time
        self.assertLess(end - start, 1.0)

    def test_rapid_key_presses_performance(self):
        """Test handling rapid key presses efficiently."""
        keyboard = Keyboard(device_id='perf_kb')
        import time
        
        start = time.time()
        with patch.object(keyboard, 'press_key'):
            for i in range(100):
                keyboard.press_key(chr(97 + (i % 26)))  # Cycle through a-z
        end = time.time()
        
        # Should handle 100 key presses quickly
        self.assertLess(end - start, 1.0)

    def test_macro_recording_performance(self):
        """Test macro recording with many events."""
        recorder = MacroRecorder()
        
        import time
        start = time.time()
        recorder.start_recording()
        for i in range(100):
            recorder.record_event(KeyEvent(key='a', pressed=(i % 2 == 0)))
        recorder.stop_recording()
        end = time.time()
        
        events = recorder.get_recorded_events()
        self.assertEqual(len(events), 100)
        # Should record 100 events quickly
        self.assertLess(end - start, 1.0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
