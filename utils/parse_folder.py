import glob, os
def parse_folder(path: str, extension=".txt") -> dict:
    file_list = {}
    for file in os.listdir(path):
        if file.endswith(extension):
            file_list[file.split('.')[0]] = file
    return file_list

