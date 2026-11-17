from typing import Any
from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)

data: list[Any] = [
    "Hello world",
    [3.14, -1, 2.71],
    [
        {
            "log_level": "WARNING",
            "log_message": "Telnet access! Use ssh instead",
        },
        {"log_level": "INFO", "log_message": "User wil is connected"},
    ],
    42,
    ["Hi", "five"],
]


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def __repr__(self) -> str:
        return "s"

    def __str__(self) -> str:
        return "pass"

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            for proc in self._processors:
                if proc.validate(data):
                    proc.ingest(data)
                    break
            else:
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {data}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return

        for proc in self._processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")

            print(
                f"{name}: total {proc._count} items processed, "
                f"remaining {len(proc._data)} on processor"
            )


""" === TEST === """


def test1(stream: DataStream) -> None:

    print("\n")
    print("Registering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    print(f"Send first batch of data on stream: {data}")
    print("\n")
    stream.process_stream(data)
    print("\n")
    stream.print_processors_stats()


def test2(stream: DataStream) -> None:

    print("\n")
    print("Registering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(data)
    print("\n")
    stream.print_processors_stats()


def test3(stream: DataStream) -> None:
    print("\nConsume some elements from the data processors:")

    for proc in stream._processors:
        name = type(proc).__name__

        if name == "NumericProcessor":
            count = 3
        elif name == "TextProcessor":
            count = 2
        else:
            count = 1
        for _ in range(count):
            proc.output()
        print("\n")
        stream.print_processors_stats()


""" === MAIN === """


def main() -> None:
    # title
    print("=== Code Nexus - Data Stream ===\n")
    # instance
    stream = DataStream()

    print("Initialize Data Stream...\n")
    stream.print_processors_stats()

    test1(stream)
    test2(stream)
    test3(stream)


if __name__ == "__main__":
    main()
