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
    sp = Semesterplan("./test2.pdf")
    sp.parse()

    files = read_pdf_folder(FOLDER_IN)

    for file in files:
        with open(os.path.join(FOLDER_OUT, file[:-4] + ".ics"), "w") as f:
            f.writelines(sp.to_ical())
            f.close()


if __name__ == "__main__":
    main()
