import os
from semesterplan import Semesterplan


FOLDER_IN = "./input"


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

        print(f"\n\033[92m————————————————————————————————————————————————————\033[0m")
        print(f"\033[92m{sp.title}\033[0m")
        print(f"\033[92m————————————————————————————————————————————————————\033[0m")
        for event in sp.events:
            print(
                f"{event.name} ( {event.start.strftime('%m-%d %H:%M')} - {event.end.strftime('%m-%d %H:%M')} ) {event.room} - {event.teacher}"
            )


if __name__ == "__main__":
    main()
