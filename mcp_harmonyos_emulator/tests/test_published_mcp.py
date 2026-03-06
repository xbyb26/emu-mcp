#!/usr/bin/env python3
"""Test published MCP server from TestPyPI using JSON-RPC protocol."""

import subprocess
import json
import sys
import os

# Set environment variables
os.environ["instancePath"] = "/Users/emu/.Huawei/Emulator/deployed"
os.environ["imageRoot"] = "/Users/emu/Library/Huawei/Sdk"


def send_request(processed, request):
    """Send a JSON-RPC request and get response."""
    request_str = json.dumps(request) + "\n"
    process.stdin.write(request_str)
    process.stdin.flush()

    # Read response
    response_line = process.stdout.readline()
    if not response_line:
        return None

    return json.loads(response_line.strip())


def main():
    print("🚀 Starting MCP server from TestPyPI (v1.0.3)...")

    # Start MCP server from TestPyPI as subprocess
    process = subprocess.Popen(
        [
            "uvx",
            "--index-url",
            "https://test.pypi.org/simple/",
            "--extra-index-url",
            "https://pypi.org/simple/",
            "mcp-harmonyos-emulator==1.0.3",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/Users/emu/Documents/code/emu-mcp/mcp_harmonyos_emulator",
    )

    # Wait for server to initialize
    import time

    time.sleep(5)

    # Check if server is still running
    if process.poll() is not None:
        stderr_output = process.stderr.read()
        print(f"❌ Server failed to start!")
        print(f"stderr: {stderr_output}")
        return

    print("✅ MCP server started from (TestPyPI)")

    # Initialize connection
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    print("\n📤 Sending initialize request...")
    try:
        response = send_request(process, init_request)
        print(f"📥 Initialize response: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"❌ Error sending initialize request: {e}")
        stderr_output = process.stderr.read()
        print(f"stderr: {stderr_output}")
        return

    # List tools
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {},
    }

    print("\n📤 Listing available tools...")
    response = send_request(process, list_tools_request)
    print(f"📥 Tools list: {json.dumps(response, indent=2)}")

    # Test list_emulator_devices
    list_devices_request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "list_emulator_devices",
            "arguments": {},
        },
    }

    print("\n📤 Listing emulator devices...")
    response = send_request(process, list_devices_request)
    print(f"📥 List devices response: {json.dumps(response, indent=2)}")

    # Test start_emulator
    start_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "start_emulator",
            "arguments": {"device_model": "Mate 80 Pro Max"},
        },
    }

    print("\n📤 Starting emulator...")
    response = send_request(process, start_request)
    print(f"📥 Start response: {json.dumps(response, indent=2)}")

    # Wait a bit
    time.sleep(2)

    # Test stop_emulator
    stop_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "stop_emulator",
            "arguments": {"device_model": "Mate 80 Pro Max"},
        },
    }

    print("\n📤 Stopping emulator...")
    response = send_request(process, stop_request)
    print(f"📥 Stop response: {json.dumps(response, indent=2)}")

    # Cleanup
    print("\n🧹 Cleaning up...")
    process.terminate()
    process.wait(timeout=5)
    print("✅ Test completed")


if __name__ == "__main__":
    main()
