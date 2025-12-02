from functions.get_file_content import get_file_content


test_cases = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py")
]

for working_dir, directory in test_cases:
    print(f'Result for "{directory}" directory:')
    print(get_file_content(working_dir, directory))
    print()
