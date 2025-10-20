import os

def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

def count_lines_in_directory(directory):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_lines += count_lines_in_file(file_path)
    return total_lines

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    total_lines = count_lines_in_directory(current_directory)
    print(f"Total lines of code: {total_lines}")
