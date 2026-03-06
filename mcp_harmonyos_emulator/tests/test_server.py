#!/usr/bin/env python3
"""
Simple test script to verify MCP server functionality.

This script tests the basic functionality of the HarmonyOS Emulator MCP server
without requiring a running MCP client.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_harmonyos_emulator import (
    StartEmulatorInput,
    StopEmulatorInput,
    InstallAppInput,
    _check_command_exists,
    _check_environment_variables
)


def print_test_header(test_name):
    """Print a formatted test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)


def test_input_models():
    """Test Pydantic input models."""
    print_test_header("Input Models Validation")

    try:
        # Test StartEmulatorInput
        start_input = StartEmulatorInput(device_model="Mate 80 Pro Max")
        print(f"✓ StartEmulatorInput created: {start_input.device_model}")

        # Test StopEmulatorInput
        stop_input = StopEmulatorInput(device_model="Mate 80 Pro Max")
        print(f"✓ StopEmulatorInput created: {stop_input.device_model}")

        # Test InstallAppInput
        install_input = InstallAppInput(app_path="/path/to/app.hap")
        print(f"✓ InstallAppInput created: {install_input.app_path}")

        print("\n✓ All input models validated successfully")
        return True
    except Exception as e:
        print(f"\n✗ Input model validation failed: {e}")
        return False


def test_environment_variables():
    """Test environment variable checking."""
    print_test_header("Environment Variables Check")

    # Test with missing variables
    os.environ.pop('instancePath', None)
    os.environ.pop('imageRoot', None)

    is_valid, error_msg = _check_environment_variables()
    if not is_valid:
        print(f"✓ Correctly detected missing env vars: {error_msg}")
    else:
        print("✗ Should have detected missing env vars")
        return False

    # Test with instancePath only
    os.environ['instancePath'] = '/test/instance'
    is_valid, error_msg = _check_environment_variables()
    if not is_valid and 'imageRoot' in error_msg:
        print(f"✓ Correctly detected missing imageRoot: {error_msg}")
    else:
        print("✗ Should have detected missing imageRoot")
        return False

    # Test with both variables
    os.environ['imageRoot'] = '/test/images'
    is_valid, error_msg = _check_environment_variables()
    if is_valid:
        print(f"✓ Environment variables validated successfully")
    else:
        print(f"✗ Should have validated successfully: {error_msg}")
        return False

    # Cleanup
    os.environ.pop('instancePath', None)
    os.environ.pop('imageRoot', None)

    return True


def test_command_check():
    """Test command existence checking."""
    print_test_header("Command Existence Check")

    # Test commands that likely don't exist
    test_cmd = "nonexistent_command_xyz"
    exists = _check_command_exists(test_cmd)
    if not exists:
        print(f"✓ Correctly detected missing command: {test_cmd}")
    else:
        print(f"✗ Should have detected missing command: {test_cmd}")
        return False

    # Test commands that likely exist
    for cmd in ['ls', 'echo', 'cat']:
        exists = _check_command_exists(cmd)
        if exists:
            print(f"✓ Found command: {cmd}")
        else:
            print(f"⚠ Command not found (may be expected): {cmd}")

    return True


def test_server_import():
    """Test that server can be imported."""
    print_test_header("Server Import Test")

    try:
        from mcp_harmonyos_emulator import mcp
        print(f"✓ MCP server imported successfully")
        print(f"  Server name: {mcp.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to import MCP server: {e}")
        return False


def test_package_installation():
    """Test if package can be installed."""
    print_test_header("Package Installation Test")

    try:
        # Try to get package info
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "mcp"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ mcp package is installed")
            return True
        else:
            print("⚠ mcp package not found. Install with: pip install mcp")
            return False
    except Exception as e:
        print(f"⚠ Could not check mcp package: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("HarmonyOS Emulator MCP Server - Test Suite")
    print("="*60)

    results = []

    # Run tests
    results.append(("Server Import", test_server_import()))
    results.append(("Package Installation", test_package_installation()))
    results.append(("Input Models", test_input_models()))
    results.append(("Environment Variables", test_environment_variables()))
    results.append(("Command Check", test_command_check()))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
