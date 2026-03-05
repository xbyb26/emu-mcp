# HarmonyOS Emulator MCP Server - Project Summary

## Project Structure

```
mcp_harmonyos_emulator/
├── src/
│   └── mcp_harmonyos_emulator/
│       └── __init__.py          # Main MCP server implementation
├── tests/
│   └── test_mcp_harmonyos_emulator.py  # Comprehensive test suite
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Python dependencies
├── smithery.yaml                 # Smithery publication configuration
├── test_server.py                # Quick test script
├── README.md                     # Documentation
└── .gitignore                   # Git ignore rules
```

## Features Implemented

### 1. MCP Server Tools

#### start_emulator
- Starts HarmonyOS emulator with specified device model
- Validates environment variables (instancePath, imageRoot)
- Checks for Emulator command availability
- Returns process ID and configuration details

#### stop_emulator
- Stops running emulator instance
- Validates device model parameter
- Checks for Emulator command availability
- Handles timeout scenarios

#### install_app
- Installs HarmonyOS applications (.hap files)
- Validates app file existence
- Checks for hdc command availability
- Handles installation timeout

### 2. Input Validation

All tools use Pydantic models for input validation:
- `StartEmulatorInput`: Validates device_model parameter
- `StopEmulatorInput`: Validates device_model parameter
- `InstallAppInput`: Validates app_path parameter

### 3. Error Handling

Comprehensive error handling for:
- Missing environment variables
- Command not found scenarios
- File not found errors
- Timeout exceptions
- Subprocess failures

### 4. Testing

**Test Coverage:**
- 19 unit tests covering all functionality
- Input model validation tests
- Environment variable checking tests
- Command existence tests
- Tool execution tests with mocked subprocess calls
- Error scenario tests

**Test Results:**
```
19 passed in 0.28s
```

## Installation & Usage

### 1. Install Dependencies

```bash
cd mcp_harmonyos_emulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Set required environment variables in your MCP client configuration:

```json
{
  "mcpServers": {
    "harmonyos-emulator": {
      "command": "python",
      "args": ["-m", "mcp_harmonyos_emulator"],
      "env": {
        "instancePath": "/path/to/emulator/instance",
        "imageRoot": "/path/to/emulator/images"
      }
    }
  }
}
```

Or set in shell:
```bash
export instancePath="/path/to/emulator/instance"
export imageRoot="/path/to/emulator/images"
```

### 3. Run Tests

```bash
# Quick test
python test_server.py

# Full test suite
pytest tests/ -v
```

### 4. Run MCP Server

```bash
python -m mcp_harmonyos_emulator
```

## Tool Usage Examples

### Start Emulator

```python
{
  "tool": "start_emulator",
  "arguments": {
    "device_model": "Mate 80 Pro Max"
  }
}
```

**Response:**
```
Successfully started HarmonyOS emulator with device model 'Mate 80 Pro Max'
Instance path: /path/to/instance
Image root: /path/to/images
Process ID: 12345
```

### Stop Emulator

```python
{
  "tool": "stop_emulator",
  "arguments": {
    "device_model": "Mate 80 Pro Max"
  }
}
```

**Response:**
```
Successfully stopped HarmonyOS emulator with device model 'Mate 80 Pro Max'
```

### Install App

```python
{
  "tool": "install_app",
  "arguments": {
    "app_path": "/path/to/application.hap"
  }
}
```

**Response:**
```
Successfully installed application from '/path/to/application.hap'
Output: Install success
```

## Publication to Smithery

The project includes `smithery.yaml` configuration for easy publication:

```bash
# Install via Smithery
npx -y @smithery/cli install @yourusername/mcp-harmonyos-emulator
```

## Prerequisites

1. **HarmonyOS SDK**: Must be installed and available in PATH
2. **Emulator Command**: `Emulator` command must be accessible
3. **HDC Command**: `hdc` command must be accessible for app installation
4. **Python 3.10+**: Required for MCP server

## Troubleshooting

### Environment Variables Not Set
**Error:** `Please configure instancePath environment variable`
**Solution:** Set instancePath and imageRoot in MCP client config or shell

### Emulator Command Not Found
**Error:** `Emulator command not found. Please ensure HarmonyOS SDK is installed and in PATH`
**Solution:** Add HarmonyOS SDK tools directory to PATH

### HDC Command Not Found
**Error:** `hdc command not found. Please ensure HarmonyOS SDK is installed and in PATH`
**Solution:** Add HarmonyOS SDK tools directory to PATH

### App File Not Found
**Error:** `Application file not found at '/path/to/app.hap'`
**Solution:** Verify the app file path is correct and the file exists

## References

- [HarmonyOS Emulator Command Line Documentation](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-emulator-command-line)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## License

Apache-2.0
