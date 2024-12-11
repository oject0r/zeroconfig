import aiofiles

class Configer:
    def __init__(self, default_config=None):
        self.config = default_config or {}
        self.current_section = self.config
        self.pending_key = None
        self.multiline_key = None
        self.multiline_value = []

    def parse_config(self, content):
        stack = [self.config]

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            self.parse_line(line, stack)

    def parse_line(self, line, stack):
        # Обработка ключей с вложенными блоками
        if self.pending_key:
            if line == "{":
                stack[-1][self.pending_key] = {}
                stack.append(stack[-1][self.pending_key])
                self.pending_key = None
            return

        # Обработка многострочных значений
        if self.multiline_key:
            if line.endswith('"""'):
                self.multiline_value.append(line[:-3].rstrip())
                stack[-1][self.multiline_key] = "\n".join(self.multiline_value)
                self.multiline_key = None
                self.multiline_value = []
            else:
                self.multiline_value.append(line)
            return

        # Начало многострочного значения
        if line.endswith('"""'):
            key = line.split()[0]
            self.multiline_key = key
            self.multiline_value = []
            return

        # Обработка вложенных блоков
        if line.endswith("{"):
            key = line.split()[0]
            stack[-1][key] = {}
            stack.append(stack[-1][key])
            return

        # Закрытие блока
        if line == "}":
            if len(stack) > 1:
                stack.pop()
            return

        # Обработка обычных ключей и значений
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            stack[-1][parts[0]] = self.parse_value(parts[1])
        elif len(parts) == 1:
            self.pending_key = parts[0]

    def parse_value(self, value):
        # Преобразуем строку в соответствующее значение
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
        return self.config

    def load_sync(self, file_path):
        # Синхронная загрузка конфигурации из файла
        self.config = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            self.parse_config(file.read())
        return self.config

    async def load_async(self, file_path):
        # Асинхронная загрузка конфигурации из файла
        self.config = {}
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            self.parse_config(await file.read())
        return self.config
