from functions.get_file_content import get_file_content
from config import READ_FILE_MAXIMUM_CHARACTERS


def main():
    # 1) lorem truncation test
    lorem_result = get_file_content("calculator", "lorem.txt")
    truncation_message = f'[...File "lorem.txt" truncated at {READ_FILE_MAXIMUM_CHARACTERS} characters]'

    if lorem_result.endswith(truncation_message):
        print("Truncation: PASSED")
    else:
        print("Truncation: FAILED")
        print(f"Expected output to end with: {truncation_message!r}")
        print(f"Actual last 120 chars: {lorem_result[-120:]!r}")

    print(f"Returned length: {len(lorem_result)}")
    print()

    # 2) required print cases
    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print()


if __name__ == "__main__":
    main()
