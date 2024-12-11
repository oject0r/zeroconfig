# ZeroConfig

**ZeroConfig** is an ultra-fast, memory-efficient, and lightweight configuration parser designed for high-performance applications. It supports both synchronous and asynchronous loading, and it can handle environment variable substitution, making it ideal for large configuration files with dynamic values. ZeroConfig uses direct string manipulation and simple data structures to provide maximum performance with minimal overhead.

## Features

- **Ultra-fast parsing**: Efficient handling of large configuration files with minimal overhead.
- **Memory-efficient**: Optimized for minimal memory usage.
- **Lightweight**: Small file size with no unnecessary dependencies.
- **Synchronous and Asynchronous loading**: Supports both blocking and non-blocking operations.
- **Flexible data types**: Automatically parses strings, integers, booleans, and floats.
- **Environment variable support**: Supports substitution of environment variables using `%VAR_NAME%`.
- **Nested dictionaries**: Allows nested sections for complex configurations.
- **Multiline values**: Supports multiline strings enclosed in triple quotes.

## Installation

You can install **ZeroConfig** by cloning the repository directly:

```bash
git clone https://github.com/oject0r/zeroconfig.git
cd zeroconfig
```

Alternatively, you can download and integrate the `configer.py` file into your project.

## Usage

### Synchronous Loading

```python
from zeroconfig import Configer

configer = Configer()
config = configer.load_sync('config.txt')

print(config['someData'])
```

### Asynchronous Loading

```python
import asyncio
from zeroconfig import Configer

async def load_config():
    configer = Configer()
    config = await configer.load_async('config.txt')
    print(config['someData'])
    

asyncio.run(load_config())
```

## Configuration File Format

The configuration files supported by **ZeroConfig** follow a simple key-value structure with optional nested sections and environment variable substitution. Example:

```ini
# Sample config file

host localhost
port 8080

# Using environment variables
database_user %DB_USER%
database_password %DB_PASSWORD%

debug true

# Nested sections
database {
    host 127.0.0.1
    port 3306
}

# Multiline values with triple quotes
description """
This is a
multiline
value.
"""
```

### Multiline Values

To define multiline values, use triple quotes:

```ini
description """
This is a
multiline
value.
"""
```

### Environment Variable Substitution

Environment variables can be referenced in the configuration using the `%VAR_NAME%` syntax. For example, if you set an environment variable `DB_USER`, you can reference it like this:

```ini
database_user %DB_USER%
```

**ZeroConfig** will automatically replace `%DB_USER%` with the value of the corresponding environment variable.

## Performance

**ZeroConfig** is designed to be highly efficient, both in terms of speed and memory usage. It can handle large configuration files without consuming unnecessary resources, making it ideal for high-performance applications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.