from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
        self._count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")

        return self._data.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(isinstance(value, (int, float)) for value in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if not isinstance(data, list):
            data = [data]

        for value in data:
            if isinstance(value, bool):
                value = int(value)

            self._data.append((self._count, str(value)))
            self._count += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(value, str) for value in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if not isinstance(data, list):
            data = [data]

        for value in data:
            self._data.append((self._count, value))
            self._count += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(value, dict) and self.validate(value)
                for value in data
            )

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if not isinstance(data, list):
            data = [data]

        for value in data:
            if "log_level" in value and "log_message" in value:
                message = f"{value['log_level']}: " f"{value['log_message']}"
            else:
                message = str(value)

            self._data.append((self._count, message))
            self._count += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    # Numeric Processor
    print("\nTesting Numeric Processor...")

    numeric = NumericProcessor()

    print("Trying to validate input '42':", numeric.validate(42))
    print("Trying to validate input 'Hello':", numeric.validate("Hello"))

    print(("Test invalid ingestion of string 'foo' without prior validation:"))

    try:
        # The subject requires an intentional mypy error for this example.
        numeric.ingest("foo")
    except ValueError as error:
        print("Got exception:", error)

    numbers: list[int | float] = [1, 2, 3, 4, 5]

    print("Processing data:", numbers)
    numeric.ingest(numbers)

    print("Extracting 3 values...")

    for _ in range(3):
        index, value = numeric.output()
        print(f"Numeric value {index}: {value}")

    # Text Processor
    print("\nTesting Text Processor...")

    text = TextProcessor()

    print("Trying to validate input '42':", text.validate(42))

    words = ["Hello", "Nexus", "World"]

    print("Trying to validate input:", words, text.validate(words))
    print("Processing data:", words)
    text.ingest(words)

    print("Extracting 1 value...")

    index, value = text.output()
    print(f"Text value {index}: {value}")

    # Log Processor
    print("\nTesting Log Processor...")

    logs = LogProcessor()

    print("Trying to validate input 'Hello':", logs.validate("Hello"))

    entries = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]

    print("Trying to validate input:", entries, logs.validate(entries))
    print("Processing data:", entries)
    logs.ingest(entries)

    print("Extracting 2 values...")

    for _ in range(2):
        index, value = logs.output()
        print(f"Log entry {index}: {value}")


if __name__ == "__main__":
    main()
