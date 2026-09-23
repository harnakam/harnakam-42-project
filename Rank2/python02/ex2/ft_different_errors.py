def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 10 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        # Intentionally mix types to demonstrate a runtime TypeError.
        _ = "water level: " + 3  # type: ignore[operator]


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for operation in (0, 1, 2, 3, 4):
        print(f"Testing operation {operation}...")
        try:
            garden_operations(operation)
            print("Operation completed successfully")
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")
    # try:
    #     garden_operations(0)
    # except (ValueError, TypeError):
    #     print("Caught grouped ValueError/TypeError as expected")
    print("All error types tested successfully!")


# def test_error_types() -> None:
#     print("=== Garden Error Types Demo ===")
#     for op in (0, 1, 2, 3, 4):
#         print(f"Testing operation {op}...")
#         try:
#             garden_operations(op)
#         except Exception as e:
#             print(f"Caught {type(e).__name__}: {e}")
#         print("Operation completed successfully")
#         print("All error types tested successfully!")

if __name__ == "__main__":
    test_error_types()
