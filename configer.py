import os
import aiofiles
import re

class Configer:
    def __init__(self, default_config=None):
        """
        Initializes the Configer class with an optional default configuration.

        Args:
            default_config (dict, optional): The initial configuration to load. Defaults to an empty dictionary.
        """
        self.config = default_config or {}
        self.current_section = self.config
        self.pending_key = None
        self.multiline_key = None
        self.multiline_value = []

    def parse_config(self, content: str):
        """
        Parses the entire content of the configuration file line by line.

        Args:
            content (str): The content of the configuration file to parse.
        """
        stack = [self.config]

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            self.parse_line(line, stack)

    def parse_line(self, line: str, stack: list):
        """
        Parses a single line of the configuration file.

        Args:
            line (str): The line to parse.
            stack (list): A stack to keep track of nested sections (dictionaries).
        """
        # Handle pending key for nested blocks
        if self.pending_key:
            if line == "{":
                stack[-1][self.pending_key] = {}
                stack.append(stack[-1][self.pending_key])
                self.pending_key = None
            return

        # Handle multiline values
        if self.multiline_key:
            if line.endswith('"""'):
                self.multiline_value.append(line[:-3].rstrip())
                stack[-1][self.multiline_key] = "\n".join(self.multiline_value)
                self.multiline_key = None
                self.multiline_value = []
            else:
                self.multiline_value.append(line)
            return

        # Start multiline string value
        if line.endswith('"""'):
            key = line.split()[0]
            self.multiline_key = key
            self.multiline_value = []
            return

        # Handle nested blocks
        if line.endswith("{"):
            key = line.split()[0]
            stack[-1][key] = {}
            stack.append(stack[-1][key])
            return

        # Close nested block
        if line == "}":
            if len(stack) > 1:
                stack.pop()
            return

        # Handle regular key-value pairs
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            value = self.replace_env_variables(parts[1])
            stack[-1][parts[0]] = self.parse_value(value)
        elif len(parts) == 1:
            self.pending_key = parts[0]

    def replace_env_variables(self, value: str) -> str:
        """
        Replaces all occurrences of %VAR_NAME% with the corresponding environment variable value.

        Args:
            value (str): The value to process.

        Returns:
            str: The value with environment variables replaced.
        """
        matches = re.findall(r"%(\w+)%", value)
        for match in matches:
            env_value = os.getenv(match)
            if env_value is not None:
                value = value.replace(f"%{match}%", env_value)
            else:
                print(f"Warning: Environment variable '{match}' not found.")
        return value

    def parse_value(self, value: str):
        """
        Parses a value from string format into its corresponding type (bool, int, float, or string).

        Args:
            value (str): The value to parse.

        Returns:
            bool, int, float, str: The parsed value, converted to the appropriate type.
        """
        value = value.strip()
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value.strip('"')

    def to_dict(self):
        """
        Converts the parsed configuration into a dictionary.

        Returns:
            dict: The configuration as a dictionary.
        """
        return self.config

    def load_sync(self, file_path: str):
        """
        Synchronously loads the configuration from a file and parses it.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            dict: The loaded and parsed configuration.
        """
        self.config = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            self.parse_config(file.read())
        return self.config

    async def load_async(self, file_path: str):
        """
        Asynchronously loads the configuration from a file and parses it.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            dict: The loaded and parsed configuration.
        """
        self.config = {}
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            self.parse_config(await file.read())
        return self.config
