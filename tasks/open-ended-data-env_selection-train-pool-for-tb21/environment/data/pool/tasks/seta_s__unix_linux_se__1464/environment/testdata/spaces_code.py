class Formatter:
    def __init__(self):
        self.indent_size = 4
        self.current_indent = 0
        self.output = []

    def indent(self):
        self.current_indent += self.indent_size

    def dedent(self):
        self.current_indent = max(0, self.current_indent - self.indent_size)

    def write(self, text):
        line = ' ' * self.current_indent + text
        self.output.append(line)
        return line

    def reset(self):
        self.current_indent = 0
        self.output = []

    def get_output(self):
        return list(self.output)

    def format_block(self, lines):
        result = []
        for line in lines:
            result.append(self.write(line))
        return result
