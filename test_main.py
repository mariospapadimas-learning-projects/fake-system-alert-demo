"""Run the original script with every desktop and OS effect replaced by mocks."""

import ast
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, call, patch


SCRIPT = Path(__file__).with_name("main.py")
REVEAL = "\nJust kidding! \U0001F604 You have NOT been hacked.\n"


class DemoTests(unittest.TestCase):
    def run_demo(self, *, enable_shutdown=False, response=7):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        if enable_shutdown:
            settings = [
                node for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name)
                        and target.id == "shutdown_in_the_end"
                        for target in node.targets)
            ]
            self.assertEqual(len(settings), 1, "Expected the public shutdown boolean")
            self.assertIs(settings[0].value.value, False)
            # Change only the in-memory test copy, never the actual setting.
            settings[0].value = ast.copy_location(ast.Constant(True), settings[0].value)

        modules = {
            "pyautogui": Mock(spec=["hotkey", "write", "press"]),
            "time": Mock(spec=["sleep"]),
            "os": Mock(spec=["system"]),
            "webbrowser": Mock(spec=["open_new_tab"]),
            "ctypes": Mock(spec=["windll"]),
            "winsound": Mock(spec=["Beep"]),
        }
        effects = Mock()
        for name, module in modules.items():
            effects.attach_mock(module, "p" if name == "pyautogui" else name)
        modules["ctypes"].windll.user32.MessageBoxW.side_effect = [1, response]
        namespace = {"__name__": "__main__"}
        with patch.dict(sys.modules, modules):
            exec(compile(tree, str(SCRIPT), "exec"), namespace)
        return namespace, effects

    def test_default_is_false_and_ending_is_harmless(self):
        namespace, effects = self.run_demo(response=6)
        self.assertIs(namespace.get("shutdown_in_the_end"), False)
        effects.os.system.assert_not_called()
        self.assertEqual(effects.ctypes.windll.user32.MessageBoxW.call_count, 1)
        self.assertEqual(effects.mock_calls[-1], call.p.write(REVEAL, interval=0.08))

    def test_original_visual_sequence_and_timing_are_preserved(self):
        _, effects = self.run_demo()
        self.assertEqual(effects.mock_calls, [
            call.ctypes.windll.user32.MessageBoxW(
                0, "Critical System Failure Detected!", "Windows Security Alert", 0x10),
            call.p.hotkey("win", "r"),
            call.p.write("cmd"),
            call.p.press("enter"),
            call.time.sleep(1),
            call.p.write("color 02"),
            call.p.press("enter"),
            call.time.sleep(1),
            call.p.write("dir/s"),
            call.p.press("enter"),
            call.time.sleep(5),
            call.webbrowser.open_new_tab(
                "https://youtu.be/xvFZjo5PgG0?si=8aTfPhxDtyrYZ5Q6"),
            call.p.hotkey("win", "r"),
            call.time.sleep(1),
            call.p.write("notepad"),
            call.p.press("enter"),
            call.time.sleep(1),
            call.p.write("YOU HAVE BEEN HACKED!!! \n"),
            call.p.write("Your pc will shut down in \n"),
            call.time.sleep(1),
            call.p.write("3\n"),
            call.winsound.Beep(1000, 300),
            call.time.sleep(1),
            call.p.write("2\n"),
            call.winsound.Beep(1000, 300),
            call.time.sleep(1),
            call.p.write("1\n"),
            call.winsound.Beep(1000, 300),
            call.time.sleep(1),
            call.p.write(REVEAL, interval=0.08),
        ])

    def test_message_has_no_payment_demand(self):
        _, effects = self.run_demo()
        messages = [entry.args[0] for entry in effects.p.write.call_args_list]
        self.assertIn("YOU HAVE BEEN HACKED!!! \n", messages)
        self.assertNotIn("PAY MONEY", "".join(messages))

    def test_decline_cancel_or_failed_confirmation_never_shuts_down(self):
        # IDNO, IDCANCEL (also Esc/close), API failure, and other non-Yes results.
        for response in (7, 2, 0, 1, -1):
            with self.subTest(response=response):
                _, effects = self.run_demo(enable_shutdown=True, response=response)
                effects.os.system.assert_not_called()
                self.assertEqual(effects.ctypes.windll.user32.MessageBoxW.call_count, 2)
                self.assertEqual(effects.mock_calls[-1], call.p.write(REVEAL, interval=0.08))

    def test_explicit_yes_is_required_after_real_shutdown_warning(self):
        _, effects = self.run_demo(enable_shutdown=True, response=6)
        confirmation = effects.ctypes.windll.user32.MessageBoxW.call_args
        self.assertEqual(confirmation.args[0], 0)
        self.assertIn("REAL shutdown", confirmation.args[1])
        self.assertIn("Save", confirmation.args[1])
        # Yes/No/Cancel, warning icon, second (No) button is default.
        self.assertEqual(confirmation.args[3], 0x133)
        effects.os.system.assert_called_once_with("shutdown /s /t 1")
        self.assertEqual(effects.mock_calls[-2:], [
            call.ctypes.windll.user32.MessageBoxW(*confirmation.args),
            call.os.system("shutdown /s /t 1"),
        ])

    def test_script_is_syntactically_valid(self):
        compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")


if __name__ == "__main__":
    unittest.main()
