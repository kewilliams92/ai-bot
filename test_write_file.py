from functions.write_file import write_file


test_cases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]

for working_dir, directory, content in test_cases:
    print(f'Result for "{directory}" directory:')
    print(write_file(working_dir, directory,content))
    print()
