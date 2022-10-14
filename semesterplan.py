from dataclasses import dataclass
import datetime as dt
import json
import re
import pdfplumber
from ics import Calendar, Event


@dataclass
class SemsterPrimitive:
    weeks: list
    day: str
    content: str
    start: str
    end: str


@dataclass
class SemesterEvent:
    name: str
    start: str
    end: str
    teacher: str
    room: str


class SemesterPage:
    def __init__(self, page):
        self.header = page.extract_text().split("\n")[:3]  # get the first 3 lines
        self.table = page.extract_table()
        self.events = []
        self.primitives = []
        self.weeks = []
        self.times = []
        self.year = ""
        self.title = ""
        self.weekdays = ["Mo", "Di", "Mi", "Do", "Fr"]

    def parse_header(self):
        self.title = self.header[0].split("für")[1].lstrip()
        self.year = self.header[1].split(" ")[1].split("/")[0]
        self.weeks = self.header[2][16:].split("Datum: ")[0].replace(" ", "").split(",")

    def parse_times(self):
        pattern = r"\d\d(\d)?\d?\d?(\d):(:):\d\d(\d)\d\d(\d)"

        for time in self.table[0][1:-1]:
            res = list(re.match(pattern, time).groups())
            res = [x for x in res if x is not None]
            self.times.append("".join(res))

    def parse_table(self):
        for row in self.table:
            self.find_primitives(row)

        for primitive in self.primitives:
            self.convert_to_event(primitive)

    def find_primitives(self, row):
        day = row[0]  # get the day of the week
        row = row[1:-1]  # remove first and last cell

        tracked_event = None
        tracking_event = False

        for idx, cell in enumerate(row):
            if isinstance(cell, str) and cell != "":
                tracking_event = True
                tracked_event = SemsterPrimitive(self.weeks, day, cell, idx, 0)

            if tracking_event and cell == "":
                tracking_event = False
                tracked_event.end = idx
                self.primitives.append(tracked_event)

    def convert_to_event(self, primitive: SemsterPrimitive):
        parts = primitive.content.split("\n")

        rooms = ", ".join(re.findall(r"C\d\d-\d.\d\d", parts[-1]))
        parts = parts[:-1]  # remove the room from the parts

        teachers = []
        for part in parts:
            if (
                part.startswith("Prof.")
                or part.startswith("Dr.")
                or part.startswith("Dipl.")
                or part.startswith("Hr.")
                or part.startswith("Fr.")
            ):
                teachers.append(part)

        parts = parts[len(teachers) :]  # remove teachers from parts

        name = " ".join(parts)

        start_time = self.times[primitive.start]
        end_time = self.times[primitive.end]
        day_num = self.weekdays.index(primitive.day) + 1

        for week in self.weeks:
            start_str = f"{self.year} {week} {day_num} {start_time}"
            start = dt.datetime.strptime(start_str, "%Y %W %w %H:%M")

            end_str = f"{self.year} {week} {day_num} {end_time}"
            end = dt.datetime.strptime(end_str, "%Y %W %w %H:%M")

            e = SemesterEvent(name, start, end, ", ".join(teachers), rooms)
            self.events.append(e)


class Semesterplan:
    def __init__(self, path):
        self.path = path
        self.pdf = pdfplumber.open(path)
        self.pages = []
        self.events = []
        self.title = ""

    def parse(self) -> list[SemesterEvent]:
        self.title = (
            self.pdf.pages[0].extract_text().split("\n")[0].split("für")[1].lstrip()
        )
        for page in self.pdf.pages:
            p = SemesterPage(page)
            p.parse_header()
            p.parse_times()
            p.parse_table()
            self.pages.append(p)
            self.events += p.events

    def to_json(self) -> str:
        data = {"title": self.title, "events": []}
        for e in self.events:
            data["events"].append(
                {
                    "title": e.name,
                    "start": e.start.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": e.end.strftime("%Y-%m-%dT%H:%M:%S"),
                    "teacher": e.teacher,
                    "room": e.room,
                },
            )
        return json.dumps(data, ensure_ascii=False, indent=4)

    def to_ics(self) -> str:
        cal = Calendar()
        for e in self.events:
            event = Event()
            event.name = e.name
            event.begin = e.start
            event.end = e.end
            event.description = f".\{e.teacher} {e.room}"
            cal.events.add(event)
        return cal

        # return cal.serialize_iter()
