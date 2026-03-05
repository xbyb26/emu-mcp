"""HarmonyOS Emulator MCP Server.

This server provides tools to manage HarmonyOS emulator instances,
including starting, stopping, and installing applications.
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional
import subprocess
import os
import sys

# Initialize the MCP server
mcp = FastMCP("harmonyos_emulator_mcp")

# Constants
EMULATOR_CMD = "Emulator"
HDC_CMD = "hdc"
DEFAULT_DEVICE_MODEL = "Mate 80 Pro Max"


def _check_command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH."""
    try:
        result = subprocess.run(
            ["which", command],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def _check_environment_variables() -> tuple[bool, Optional[str]]:
    """Check if required environment variables are set.

    Returns:
        tuple: (is_valid, error_message)
    """
    instance_path = os.environ.get("instancePath")
    image_root = os.environ.get("imageRoot")

    if not instance_path:
        return False, "Please configure the instancePath environment variable"

    if not image_root:
        return False, "Please configure the imageRoot environment variable"

    return True, None


@mcp.tool(
    name="start_emulator",
    annotations={
        "title": "Start HarmonyOS Emulator",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def start_emulator(device_model: str) -> str:
    '''Start a HarmonyOS emulator instance.

    This tool launches a HarmonyOS emulator with the specified device model.
    It requires the instancePath and imageRoot environment variables to be configured.

    Args:
        device_model (str): Device model name (e.g., "Mate 80 Pro Max")

    Returns:
        str: Success message with emulator startup details or error message

    Examples:
        - Use when: "Start the HarmonyOS emulator" -> device_model="Mate 80 Pro Max"
        - Use when: "Launch emulator for testing" -> device_model="Mate 80 Pro Max"
        - Don't use when: Emulator is already running (check status first)
        - Don't use when: You need to install an app (use install_app after starting emulator)

    Error Handling:
        - Returns error if instancePath environment variable is not set
        - Returns error if imageRoot environment variable is not set
        - Returns error if Emulator command is not found in PATH
        - Returns error if emulator fails to start
    '''
    try:
        # Check environment variables
        is_valid, error_msg = _check_environment_variables()
        if not is_valid:
            return f"Error: {error_msg}"

        # Check if Emulator command exists
        if not _check_command_exists(EMULATOR_CMD):
            return f"Error: {EMULATOR_CMD} command not found. Please ensure HarmonyOS SDK is installed and in PATH"

        instance_path = os.environ.get("instancePath")
        image_root = os.environ.get("imageRoot")

        # Build the emulator command
        cmd = [
            EMULATOR_CMD,
            "-hvd",
            device_model,
            "-path",
            instance_path,
            "-imageRoot",
            image_root
        ]

        # Start the emulator in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait a moment to check if it started successfully
        import time
        time.sleep(2)

        if process.poll() is None:
            return f"Successfully started HarmonyOS emulator with device model '{device_model}'\n" \
                   f"Instance path: {instance_path}\n" \
                   f"Image root: {image_root}\n" \
                   f"Process ID: {process.pid}"
        else:
            stdout, stderr = process.communicate()
            error_msg = stderr.strip() if stderr.strip() else stdout.strip()
            return f"Error: Failed to start emulator. {error_msg}"

    except Exception as e:
        return f"Error: Unexpected error occurred while starting emulator: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="stop_emulator",
    annotations={
        "title": "Stop HarmonyOS Emulator",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def stop_emulator(device_model: str) -> str:
    '''Stop a running HarmonyOS emulator instance.

    This tool stops a running HarmonyOS emulator with the specified device model.

    Args:
        device_model (str): Device model name to stop (e.g., "Mate 80 Pro Max")

    Returns:
        str: Success message or error message

    Examples:
        - Use when: "Stop the HarmonyOS emulator" -> device_model="Mate 80 Pro Max"
        - Use when: "Shut down emulator after testing" -> device_model="Mate 80 Pro Max"
        - Don't use when: Emulator is not running
        - Don't use when: You need to continue using the emulator

    Error Handling:
        - Returns error if Emulator command is not found in PATH
        - Returns error if emulator is not running
        - Returns error if stop command fails
    '''
    try:
        # Check if Emulator command exists
        if not _check_command_exists(EMULATOR_CMD):
            return f"Error: {EMULATOR_CMD} command not found. Please ensure HarmonyOS SDK is installed and in PATH"

        # Build the stop command
        cmd = [
            EMULATOR_CMD,
            "-stop",
            device_model
        ]

        # Execute the stop command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return f"Successfully stopped HarmonyOS emulator with device model '{device_model}'"
        else:
            error_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
            return f"Error: Failed to stop emulator. {error_msg}"

    except subprocess.TimeoutExpired:
        return f"Error: Stop command timed out for device model '{device_model}'"
    except Exception as e:
        return f"Error: Unexpected error occurred while stopping emulator: {type(e).__name__}: {str(e)}"


@mcp.tool(
    name="install_app",
    annotations={
        "title": "Install HarmonyOS Application",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def install_app(app_path: str) -> str:
    '''Install a HarmonyOS application on the emulator.

    This tool installs a HarmonyOS application package (.hap) on the running emulator.
    The emulator must be running before installing an application.

    Args:
        app_path (str): Path to the HarmonyOS application package file (.hap)

    Returns:
        str: Success message with installation details or error message

    Examples:
        - Use when: "Install app.hap on the emulator" -> app_path="/path/to/app.hap"
        - Use when: "Deploy the application for testing" -> app_path="/path/to/app.hap"
        - Don't use when: Emulator is not running (start emulator first)
        - Don't use when: App file does not exist or is invalid

    Error Handling:
        - Returns error if hdc command is not found in PATH
        - Returns error if app file does not exist
        - Returns error if installation fails
    '''
    try:
        # Check if app file exists
        if not os.path.exists(app_path):
            return f"Error: Application file not found at '{app_path}'"

        # Check if hdc command exists
        if not _check_command_exists(HDC_CMD):
            return f"Error: {HDC_CMD} command not found. Please ensure HarmonyOS SDK is installed and in PATH"

        # Build the install command
        cmd = [
            HDC_CMD,
            "install",
            app_path
        ]

        # Execute the install command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            return f"Successfully installed application from '{app_path}'\n" \
                   f"Output: {output}"
        else:
            error_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
            return f"Error: Failed to install application. {error_msg}"

    except subprocess.TimeoutExpired:
        return f"Error: Installation timed out for application '{app_path}'"
    except Exception as e:
        return f"Error: Unexpected error occurred while installing application: {type(e).__name__}: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
