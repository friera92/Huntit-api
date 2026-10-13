"""Isolated launcher checks; no application servers or database are started."""
import contextlib
import io
import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import run_local


class LauncherTests(unittest.TestCase):
    def servers(self):
        return [("Django", Mock(poll=Mock(return_value=None)), 8000),
                ("Angular", Mock(poll=Mock(return_value=None)), 4200)]

    def test_environment_disables_first_run_prompts_without_changing_parent(self):
        with patch.dict(os.environ, {"NG_CLI_ANALYTICS": "true", "CUSTOM_SETTING": "kept"}, clear=True):
            environment = run_local.child_environment(True)
            self.assertEqual(environment["HUNTIT_HTTPS"], "true")
            for key in ("NG_CLI_ANALYTICS", "NG_FORCE_TTY", "NG_FORCE_AUTOCOMPLETE"):
                self.assertEqual(environment[key], "false")
            self.assertEqual(environment["CUSTOM_SETTING"], "kept")
            self.assertEqual(os.environ["NG_CLI_ANALYTICS"], "true")
            self.assertEqual(run_local.child_environment(False)["HUNTIT_HTTPS"], "false")

    def test_port_check_closes_successful_connection(self):
        connection = MagicMock()
        with patch.object(run_local.socket, "create_connection", return_value=connection) as connect:
            self.assertTrue(run_local.port_is_open(4200))
        connect.assert_called_once_with(("127.0.0.1", 4200), timeout=0.2)
        connection.__exit__.assert_called_once()

    def test_port_check_handles_connection_refused(self):
        with patch.object(run_local.socket, "create_connection", side_effect=ConnectionRefusedError):
            self.assertFalse(run_local.port_is_open(4200))

    def test_busy_port_reports_stop_instruction(self):
        with patch.object(run_local, "port_is_open", side_effect=[False, True]):
            with self.assertRaisesRegex(RuntimeError, "Port 4200.*Ctrl\\+C"):
                run_local.ensure_ports_available()

    def test_readiness_waits_for_both_servers(self):
        with patch.object(run_local, "port_is_open", side_effect=[True, False, True, True]) as check:
            with patch.object(run_local.time, "sleep") as sleep:
                run_local.wait_for_servers(self.servers())
        self.assertEqual([call.args[0] for call in check.call_args_list], [8000, 4200, 8000, 4200])
        sleep.assert_called_once_with(0.25)

    def test_early_exit_names_failed_server_even_when_exit_code_is_zero(self):
        servers = self.servers()
        servers[1][1].poll.return_value = 0
        with patch.object(run_local, "port_is_open") as check:
            with self.assertRaisesRegex(RuntimeError, "Angular stopped during startup \\(exit code 0\\)"):
                run_local.wait_for_servers(servers)
        check.assert_not_called()

    def test_startup_timeout_reports_diagnostics(self):
        with patch.object(run_local, "port_is_open", return_value=False):
            with patch.object(run_local.time, "monotonic", side_effect=[100, 280]):
                with self.assertRaisesRegex(RuntimeError, "within 180 seconds.*messages above"):
                    run_local.wait_for_servers(self.servers())

    def test_output_is_prefixed_and_stream_closed(self):
        output = io.StringIO()
        stream = io.StringIO("Building...\nReady\n")
        with contextlib.redirect_stdout(output):
            run_local.forward_output("Angular", stream)
        self.assertEqual(output.getvalue(), "[Angular] Building...\n[Angular] Ready\n")
        self.assertTrue(stream.closed)

    def test_windows_output_encoding_does_not_interrupt_log_drain(self):
        data = io.BytesIO()
        output = io.TextIOWrapper(data, encoding="cp1252", newline="\n", write_through=True)
        stream = io.StringIO("\u221a Build complete\nSecond log line\n\u221a Ready\n")
        with contextlib.redirect_stdout(output):
            run_local.forward_output("Angular", stream)
        self.assertEqual(
            data.getvalue().decode("cp1252"),
            "[Angular] ? Build complete\n[Angular] Second log line\n[Angular] ? Ready\n",
        )
        self.assertTrue(stream.closed)


if __name__ == "__main__":
    unittest.main()
