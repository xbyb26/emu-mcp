# HarmonyOS Emulator MCP Server

MCP server for managing HarmonyOS emulator instances, enabling agents to start, stop, and install applications on HarmonyOS emulators.

## Features

- **Start Emulator**: Launch HarmonyOS emulator with specified device model
- **Stop Emulator**: Stop running emulator instance
- **Install App**: Install HarmonyOS applications on the emulator

## Installation

### Standard Installation

```bash
pip install mcp-harmonyos-emulator==1.0.0
```

### OpenCode Configuration

Add the following entry to your OpenCode configuration file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "harmonyos-emulator": {
      "type": "stdio",
      "command": [
        "uvx",
        "--index-url", "https://test.pypi.org/simple/",
        "--extra-index-url", "https://pypi.org/simple/",
        "mcp-harmonyos-emulator==1.0.0"
      ],
      "enabled": true,
      "environment": {
        "instancePath": "/path/to/emulator/instance",
        "imageRoot": "/path/to/emulator/images"
      }
    }
```

This configuration uses `uvx` to automatically download and run the package from Test PyPI.

## Environment Variables

The server requires two environment variables to be configured:

- `instancePath`: Path to the emulator instance directory
- `imageRoot`: Path to the emulator image directory

These can be set in your MCP client configuration or in your shell environment:

```bash
export instancePath="/path/to/emulator/instance"
export imageRoot="/path/to/emulator/images"
```

## Usage

### Available Tools

#### 1. start_emulator

Start a HarmonyOS emulator instance.

**Parameters:**
- `device_model` (string, required): Device model name (e.g., "Mate 80 Pro Max")

**Example:**
```python
{
  "device_model": "Mate 80 Pro Max"
}
```

#### 2. stop_emulator

Stop a running HarmonyOS emulator instance.

**Parameters:**
- `device_model` (string, required): Device model name to stop (e.g., "Mate 80 Pro Max")

**Example:**
```python
{
  "device_model": "Mate 80 Pro Max"
}
```

#### 3. install_app

Install a HarmonyOS application on the emulator.

**Parameters:**
- `app_path` (string, required): Path to the application package file (.hap)

**Example:**
```python
{
  "app_path": "/path/to/application.hap"
}
```

## Prerequisites

1. **HarmonyOS SDK**: Ensure you have the HarmonyOS SDK installed
2. **Emulator Command**: The `Emulator` command must be available in your PATH
3. **HDC Command**: The `hdc` command must be available in your PATH for app installation
4. **Environment Variables**: Configure `instancePath` and `imageRoot` as described above

## Development

### Running for Development

```bash
# From project root
python -m mcp_harmonyos_emulator
```

### Running Tests

```bash
pytest tests/
```

## Troubleshooting

### Common Issues

**1. Environment variables not set**
- Error: "Please configure the instancePath environment variable"
- Solution: Set `instancePath` and `imageRoot` in your MCP client configuration or shell environment

**2. Emulator command not found**
- Error: "Emulator command not found. Please ensure HarmonyOS SDK is installed and in PATH"
- Solution: Add HarmonyOS SDK tools directory to your PATH

**3. HDC command not found**
- Error: "hdc command not found. Please ensure HarmonyOS SDK is installed and in PATH"
- Solution: Add HarmonyOS SDK tools directory to your PATH

## License

Apache-2.0

## References

- [HarmonyOS Emulator Command Line Documentation](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-emulator-command-line)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
