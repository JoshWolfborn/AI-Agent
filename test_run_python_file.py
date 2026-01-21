from functions.run_python_file import run_python_file


if __name__ == "__main__":
    print("Result for main.py (usage instructions):")
    print(run_python_file("calculator", "main.py"))
    print()

    print('Result for main.py with args ["3 + 5"] (calculator run):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Result for tests.py (run calculator tests):")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Result for ../main.py (should fail: outside working directory):")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Result for nonexistent.py (should fail: missing file):")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Result for lorem.txt (should fail: not a Python file):")
    print(run_python_file("calculator", "lorem.txt"))
    print()
