import os

parent_directory = os.path.join(os.getcwd(), "..")
file_name = os.path.join(parent_directory, "references/example.txt")

with open(file_name, 'w') as file:
    file.write('test text 0112')