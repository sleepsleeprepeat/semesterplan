from dataclasses import dataclass
import datetime
from semesterplan import Semesterplan


@dataclass
class CompressorEvent:
    name: str
    audience: list[str]
    room: str
    teacher: str
    dates: list[(datetime.datetime, datetime.datetime)]


def main():
    file = "input/1.sem_e-technik-1.pdf"

    sp = Semesterplan(file)
    sp.parse()
    print(f"\033[92m{sp.title}\033[0m")

    compressed_events = []
    for event in sp.events:
        if event.name in [ce.name for ce in compressed_events]:
            # add the date to the existing event
            for ce in compressed_events:
                if ce.name == event.name:
                    ce.dates.append((event.start, event.end))
            continue
        else:
            compressed_events.append(
                CompressorEvent(
                    event.name,
                    event.room,
                    event.teacher,
                    [(event.start, event.end)],
                )
            )
            # print(f"\033[90m{event.start.strftime('%d.%m %H:%M')}\033[0m {event.name}")

    for ce in compressed_events:
        print(f"\033[90m{len(ce.dates)}\033[0m {ce.name}")


if __name__ == "__main__":
    main()
