from semesterplan import Semesterplan


def main():
    sp = Semesterplan("./input/1.sem_e-technik-1.pdf")
    sp.parse()

    for e in sp.events:
        print(f"{e.name} → {e.start} - {e.end}")
        pass


if __name__ == "__main__":
    main()
