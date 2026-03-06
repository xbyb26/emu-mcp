# AGENTS.md - Agent Development Guidelines

## Project Overview

This is a Python MCP (Model Context Protocol) server for managing HarmonyOS emulator instances. The server provides tools to list available devices, start, stop, and install applications on HarmonyOS emulators.

**Project Type**: Python MCP Server
**Main Package**: `mcp_harmonyos_emulator`
**Python Version**: 3.10+

## Build, Lint, and Test Commands

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_mcp_harmonyos_emulator.py

# Run with verbose output
pytest tests/ -v

# Run specific test class
pytest tests/test_mcp_harmonyos_emulator.py::TestStartEmulator

# Run specific test method
pytest tests/test_mcp_harmonyos_emulator.py::TestStartEmulator::test_start_emulator_success
```

### Development
```bash
# Run the MCP server for development
python -m mcp_harmonyos_emulator

# Build the package
python -m build

# Install in development mode
pip install -e .
```

## Code Style Guidelines

### Formatting and Imports

**Import Order**: Standard library → Third-party → Local modules
```python
import os
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP
import subprocess

from mcp_harmonyos_emulator import _check_command_exists
```

**Line Length**: No explicit limit, but keep lines readable (~88-100 chars preferred)

**Quotes**: Use double quotes for strings and docstrings

**Indentation**: 4 spaces (standard Python)

### Type Hints

- Use explicit type hints for function parameters and return values
- Use `Optional[T]` for nullable types
- Use modern tuple syntax: `tuple[bool, Optional[str]]`
- Type hints are mandatory for all public functions

```python
def _check_command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH."""
    pass

async def start_emulator(device_model: str) -> str:
    """Start a HarmonyOS emulator instance."""
    pass
```

### Naming Conventions

**Functions and Variables**: `snake_case`
```python
def start_emulator(device_model: str) -> str:
    instance_path = os.environ.get("instancePath")
```

**Classes**: `PascalCase`
```python
class TestStartEmulator:
    """Test start_emulator tool."""
```

**Constants**: `UPPER_SNAKE_CASE`
```python
EMULATOR_CMD = "Emulator"
HDC_CMD = "hdc"
```

**Private Functions**: `_prefix`
```python
def _check_command_exists(command: str) -> bool:
    pass
```

### Docstrings

- Use triple double quotes for docstrings
- Include Args, Returns, and Examples sections for public functions
- Keep docstrings concise but informative

```python
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
        - Don't use when: Emulator is already running (check status first)

    Error Handling:
        - Returns error if instancePath environment variable is not set
        - Returns error if Emulator command is not found in PATH
    '''
```

### Error Handling

- Use try/except blocks for external command execution
- Return error messages as strings (not raise exceptions) for MCP tools
- Catch specific exception types when possible
- Include error context in error messages

```python
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        return "Success message"
    else:
        error_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
        return f"Error: Failed to execute. {error_msg}"
except subprocess.TimeoutExpired:
    return f"Error: Command timed out"
except Exception as e:
    return f"Error: Unexpected error: {type(e).__name__}: {str(e)}"
```

### Async/Await

- All MCP tool functions must be `async def`
- Use `@pytest.mark.asyncio` for async test functions
- Configure pytest with `asyncio_mode = "auto"` in pyproject.toml

```python
@mcp.tool(name="start_emulator")
async def start_emulator(device_model: str) -> str:
    """Start a HarmonyOS emulator instance."""
    pass
```

### Testing

- Use pytest for testing
- Use `unittest.mock` for mocking external dependencies
- Test file naming: `test_*.py`
- Test class naming: `Test<ClassName>`
- Test method naming: `test_<method_name>_<scenario>`

```python
import pytest
from unittest.mock import patch, MagicMock

class TestStartEmulator:
    """Test start_emulator tool."""

    @pytest.mark.asyncio
    @patch('mcp_harmonyos_emulator._check_command_exists')
    @patch('mcp_harmonyos_emulator.subprocess.Popen')
    async def test_start_emulator_success(self, mock_popen, mock_check_cmd):
        """Test successful emulator start."""
        mock_check_cmd.return_value = True
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        result = await start_emulator("Mate 80 Pro Max")
        assert "Successfully started" in result
```

### Environment Variables

- Required environment variables: `instancePath`, `imageRoot`
- Use `os.environ.get()` to access environment variables
- Validate environment variables before use

```python
instance_path = os.environ.get("instancePath")
if not instance_path:
    return "Error: Please configure the instancePath environment variable"
```

## Project Structure

```
mcp_harmonyos_emulator/
├── src/
│   └── mcp_harmonyos_emulator/
│       └── __init__.py          # Main MCP server implementation
├── tests/
│   ├── test_mcp_harmonyos_emulator.py  # Unit tests
│   ├── test_mcp_client.py       # MCP client integration tests
│   └── test_published_mcp.py    # Published package tests
├── pyproject.toml               # Project configuration
├── README.md                    # Project documentation
└── venv/                        # Virtual environment (gitignored)
```

## Key Dependencies

- `mcp>=0.8.0`: Model Context Protocol server framework
- `pytest>=7.0.0`: Testing framework
- `pytest-asyncio>=0.21.0`: Async test support

## MCP Tool Guidelines

- Use `@mcp.tool()`` decorator to register tools
- Include annotations for tool metadata (title, readOnlyHint, etc.)
- Return string responses (success or error messages)
- Validate inputs before execution
- Check for required commands and environment variables

```python
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
    """Tool implementation."""
    pass
```

## Common Patterns

### Subprocess Execution

```python
# Background process (emulator start)
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Synchronous execution (emulator stop, app install)
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=30
)
```

### Command Existence Check

```python
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
```

## Notes

- No explicit linting configuration (no .ruff.toml, .black.toml, or .pylintrc found)
- Follow PEP 8 guidelines where not specified above
- Use subprocess for all external command execution
- All MCP tools are async functions
- Error messages should be user-friendly and actionable

## Available Tools

### 1. list_emulator_devices

List available HarmonyOS emulator device models.

**Usage:**
```python
result = await list_emulator_devices()
```

**Returns:**
- String with numbered list of available device models
- Error message if command fails

**Example output:**
```
Available emulator devices:
  1. Mate 80 Pro Max
  2. mate80
```

### 2. start_emulator

Start a HarmonyOS emulator instance.

**Usage:**
```python
result = await start_emulator(device_model="Mate 80 Pro Max Max")
```

**Parameters:**
- `device_model` (str): Device model name from list_emulator_devices

**Returns:**
- Success message with process details
- Error message if startup fails

### 3. stop_emulator

Stop a running HarmonyOS emulator instance.

**Usage:**
```python
result = await stop_emulator(device_model="Mate 80 Pro Max Max")
```

### 4. install_app

Install a HarmonyOS application on emulator.

**Usage:**
```python
result = await install_app(app_path="/path/to/app.hap")
```

## Tool Annotations Guide

- `readOnlyHint`: True for read-only operations (list), False for mutations
- `destructiveHint`: True for destructive operations (none currently)
- `idempotentHint`: True for idempotent operations (list, stop), False otherwise
- `openWorldHint`: True for operations that interact with external world
