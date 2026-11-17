from typing import Any, Protocol
from data_processor import NumericProcessor, TextProcessor, LogProcessor
from data_stream import DataStream as BaseDataStream


data1: list[Any] = [
    "Hello world",
    [3.14, -1, 2.71],
    [
        {
            "log_level": "WARNING",
            "log_message": "Telnet access! Use ssh instead"
        },
        {
            "log_level": "INFO",
            "log_message": "User wil is connected"
        }
    ],
    42,
    ["Hi", "five"]
]

data2: list[Any] = [
    21,
    ["I love AI", "LLMs are wonderful", "Stay healthy"],
    [
        {
            "log_level": "ERROR",
            "log_message": "500 server crash"
        },
        {
            "log_level": "NOTICE",
            "log_message": "Certificate expires in 10 days"
        }
    ],
    [32, 42, 64, 84, 128, 168],
    "World hello"
]


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataStream(BaseDataStream):
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            data: list[tuple[int, str]] = []

            for _ in range(min(nb, len(proc._data))):
                data.append(proc.output())

            plugin.process_output(data)


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        out = self.format(data)
        print(out)

    @staticmethod
    def escape(value: str) -> str:
        result = ""

        for char in value:
            code = ord(char)

            if char == '"':
                result += '\\"'
            elif char == "\\":
                result += "\\\\"
            elif char == "\b":
                result += "\\b"
            elif char == "\f":
                result += "\\f"
            elif char == "\n":
                result += "\\n"
            elif char == "\r":
                result += "\\r"
            elif char == "\t":
                result += "\\t"
            elif code < 32:
                # \u -> Unicode
                # 0 -> 空いた桁を0で埋める
                # 4 -> 最小4桁
                # x -> 16進数小文字
                result += f"\\u{code:04x}"
            else:
                result += char

        return result

    @staticmethod
    def format(data: list[tuple[int, str]]) -> str:
        items: list[str] = []

        for index, value in data:
            escaped = JSONPlugin.escape(value)
            items.append(f'"item_{index}": "{escaped}"')

        return "{" + ", ".join(items) + "}"


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        out = self.format(data)
        print(out)

    @staticmethod
    def escape(value: str) -> str:
        if (
            "," in value
            or '"' in value
            or "\n" in value
            or "\r" in value
        ):
            return '"' + value.replace('"', '""') + '"'

        return value

    @staticmethod
    def format(data: list[tuple[int, str]]) -> str:
        return ",".join(
            CSVPlugin.escape(value)
            for _, value in data
        )


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")

    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)

    print(f"\nSend first batch of data on stream: {data1}")

    stream.process_stream(data1)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")

    stream.output_pipeline(3, CSVPlugin())
    stream.print_processors_stats()

    print(f"\nSend another batch of data: {data2}")

    stream.process_stream(data2)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")

    stream.output_pipeline(5, JSONPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
