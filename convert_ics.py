import os
from semesterplan import Semesterplan

FOLDER_IN = "./input"
FOLDER_OUT = "./output_ics"


def read_pdf_folder(folder_name):
    directory = os.fsencode(folder_name)
    file_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):
            file_list.append(filename)
    return file_list


def main():
    files = read_pdf_folder(FOLDER_IN)

    for file in files:
        sp = Semesterplan(os.path.join(FOLDER_IN, file))
        sp.parse()

        path = os.path.join(FOLDER_OUT, file[:-4] + ".ics")
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(sp.to_ics())
            f.close()

        print(f"Created ics file {file[:-4] + '.ics'}")


if __name__ == "__main__":
    main()
