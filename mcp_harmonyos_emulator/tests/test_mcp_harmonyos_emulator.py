"""Test suite for HarmonyOS Emulator MCP Server."""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_harmonyos_emulator import (
    StartEmulatorInput,
    StopEmulatorInput,
    InstallAppInput,
    _check_command_exists,
    _check_environment_variables,
    start_emulator,
    stop_emulator,
    install_app
)


class TestInputModels:
    """Test Pydantic input models."""

    def test_start_emulator_input_valid(self):
        """Test valid StartEmulatorInput."""
        input_data = {"device_model": "Mate 80 Pro Max"}
        model = StartEmulatorInput(**input_data)
        assert model.device_model == "Mate 80 Pro Max"

    def test_start_emulator_input_missing_field(self):
        """Test Start missing device_model field."""
        with pytest.raises(Exception):
            StartEmulatorInput()

    def test_start_emulator_input_empty_device_model(self):
        """Test empty device_model."""
        with pytest.raises(Exception):
            StartEmulatorInput(device_model="")

    def test_stop_emulator_input_valid(self):
        """Test valid StopEmulatorInput."""
        input_data = {"device_model": "Mate 80 Pro Max"}
        model = StopEmulatorInput(**input_data)
        assert model.device_model == "Mate 80 Pro Max"

    def test_install_app_input_valid(self):
        """Test valid InstallAppInput."""
        input_data = {"app_path": "/path/to/app.hap"}
        model = InstallAppInput(**input_data)
        assert model.app_path == "/path/to/app.hap"

    def test_install_app_input_empty_path(self):
        """Test empty app_path."""
        with pytest.raises(Exception):
            InstallAppInput(app_path="")


class TestUtilityFunctions:
    """Test utility functions."""

    @patch('subprocess.run')
    def test_check_command_exists_true(self, mock_run):
        """Test command exists."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = _check_command_exists("test_cmd")
        assert result is True
        mock_run.assert_called_once_with(["which", "test_cmd"], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_check_command_exists_false(self, mock_run):
        """Test command does not exist."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = _check_command_exists("test_cmd")
        assert result is False

    @patch.dict(os.environ, {'instancePath': '/path/to/instance', 'imageRoot': '/path/to/images'})
    def test_check_environment_variables_valid(self):
        """Test environment variables are set."""
        is_valid, error_msg = _check_environment_variables()
        assert is_valid is True
        assert error_msg is None

    @patch.dict(os.environ, {}, clear=True)
    def test_check_environment_variables_missing_instance_path(self):
        """Test missing instancePath."""
        is_valid, error_msg = _check_environment_variables()
        assert is_valid is False
        assert "instancePath" in error_msg

    @patch.dict(os.environ, {'instancePath': '/path/to/instance'})
    def test_check_environment_variables_missing_image_root(self):
        """Test missing imageRoot."""
        is_valid, error_msg = _check_environment_variables()
        assert is_valid is False
        assert "imageRoot" in error_msg


class TestStartEmulator:
    """Test start_emulator tool."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {'instancePath': '/path/to/instance', 'imageRoot': '/path/to/images'})
    @patch('mcp_harmonyos_emulator._check_command_exists')
    @patch('mcp_harmonyos_emulator.subprocess.Popen')
    @patch('time.sleep')
    async def test_start_emulator_success(self, mock_sleep, mock_popen, mock_check_cmd):
        """Test successful emulator start."""
        mock_check_cmd.return_value = True

        mock_process = MagicMock()
        mock_process.poll.return_value = None  # Still running
        mock_process.pid = 12345
        mock_popen.return_value = mock_process

        params = StartEmulatorInput(device_model="Mate 80 Pro Max")
        result = await start_emulator(params)

        assert "Successfully started" in result
        assert "Mate 80 Pro Max" in result
        assert "12345" in result

        # Verify command was built correctly
        cmd_args = mock_popen.call_args[0][0]
        assert cmd_args[0] == "Emulator"
        assert cmd_args[2] == "Mate 80 Pro Max"
        assert cmd_args[4] == "/path/to/instance"
        assert cmd_args[6] == "/path/to/images"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {}, clear=True)
    async def test_start_emulator_missing_env_vars(self):
        """Test start with missing environment variables."""
        params = StartEmulatorInput(device_model="Mate 80 Pro Max")
        result = await start_emulator(params)

        assert "Error:" in result
        assert "instancePath" in result

    @pytest.mark.asyncio
    @patch.dict(os.environ, {'instancePath': '/path/to/instance', 'imageRoot': '/path/to/images'})
    @patch('mcp_harmonyos_emulator._check_command_exists')
    async def test_start_emulator_command_not_found(self, mock_check_cmd):
        """Test start when Emulator command not found."""
        mock_check_cmd.return_value = False

        params = StartEmulatorInput(device_model="Mate 80 Pro Max")
        result = await start_emulator(params)

        assert "Error:" in result
        assert "Emulator command not found" in result


class TestStopEmulator:
    """Test stop_emulator tool."""

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator._check_command_exists')
    @patch('mcp_harmonyos_emulator.subprocess.run')
    async def test_stop_emulator_success(self, mock_run, mock_check_cmd):
        """Test successful emulator stop."""
        mock_check_cmd.return_value = True

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        params = StopEmulatorInput(device_model="Mate 80 Pro Max")
        result = await stop_emulator(params)

        assert "Successfully stopped" in result
        assert "Mate 80 Pro Max" in result

        # Verify command was built correctly
        cmd_args = mock_run.call_args[0][0]
        assert cmd_args[0] == "Emulator"
        assert cmd_args[1] == "-stop"
        assert cmd_args[2] == "Mate 80 Pro Max"

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator._check_command_exists')
    async def test_stop_emulator_command_not_found(self, mock_check_cmd):
        """Test stop when Emulator command not found."""
        mock_check_cmd.return_value = False

        params = StopEmulatorInput(device_model="Mate 80 Pro Max")
        result = await stop_emulator(params)

        assert "Error:" in result
        assert "Emulator command not found" in result


class TestInstallApp:
    """Test install_app tool."""

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator.os.path.exists')
    @patch('mcp_harmonyos_emulator._check_command_exists')
    @patch('mcp_harmonyos_emulator.subprocess.run')
    async def test_install_app_success(self, mock_run, mock_check_cmd, mock_exists):
        """Test successful app installation."""
        mock_exists.return_value = True
        mock_check_cmd.return_value = True

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Install success"
        mock_run.return_value = mock_result

        params = InstallAppInput(app_path="/path/to/app.hap")
        result = await install_app(params)

        assert "Successfully installed" in result
        assert "/path/to/app.hap" in result

        # Verify command was built correctly
        cmd_args = mock_run.call_args[0][0]
        assert cmd_args[0] == "hdc"
        assert cmd_args[1] == "install"
        assert cmd_args[2] == "/path/to/app.hap"

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator.os.path.exists')
    async def test_install_app_file_not_found(self, mock_exists):
        """Test install when app file does not exist."""
        mock_exists.return_value = False

        params = InstallAppInput(app_path="/path/to/nonexistent.hap")
        result = await install_app(params)

        assert "Error:" in result
        assert "not found" in result

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator.os.path.exists')
    @patch('mcp_harmonyos_emulator._check_command_exists')
    async def test_install_app_hdc_not_found(self, mock_check_cmd, mock_exists):
        """Test install when hdc command not found."""
        mock_exists.return_value = True
        mock_check_cmd.return_value = False

        params = InstallAppInput(app_path="/path/to/app.hap")
        result = await install_app(params)

        assert "Error:" in result
        assert "hdc command not found" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
