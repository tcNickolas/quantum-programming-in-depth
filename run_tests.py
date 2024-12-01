import os
import subprocess

def find_test_dirs(root_dir, chapter, lang):
    entries = os.listdir(root_dir)
    chapter_folder = [entry for entry in entries 
              if os.path.isdir(os.path.join(root_dir, entry)) 
              and entry.startswith(chapter)][0]

    test_dirs = []
    for dirpath, _, filenames in os.walk(os.path.join(root_dir, chapter_folder, lang)):
        if any(filename.startswith('test_') and filename.endswith('.py') for filename in filenames):
            test_dirs.append(dirpath)
    return test_dirs


def run_pytest_in_dir(directory):
    print(f"Running pytest in {directory}")
    res = subprocess.run(['pytest'], cwd=directory, check=True)
    if res.returncode != 0:
        print("Test failed!")
        exit()


root_directory = '.'
# Chapter 8 tests run for a longer time, so they're not included by default
for chapter in range(2, 8):
    print(f"Testing chapter {chapter}")
    for lang in ['qiskit', 'qsharp']:
        print(f"Testing {lang}")
        test_directories = find_test_dirs(root_directory, str(chapter), lang)
        test_directories.sort()

        for directory in test_directories:
            run_pytest_in_dir(directory)
