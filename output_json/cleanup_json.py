import os


FOLDER_IN = "./output_json"
FOLDER_OUT = "./output_json_clean"


def read_pdf_folder(folder_name):
    directory = os.fsencode(folder_name)
    file_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):
            file_list.append(filename)
    return file_list


def main():
    for file 


if __name__ == "__main__":
    main()
    print("Done")
