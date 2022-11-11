import re
from semesterplan import Semesterplan


def cleanup(sp: Semesterplan):
    for idx, event in enumerate(sp.events):
        # entfernen vom Tag der Deutschen Einheit
        if event.name.startswith("- Prof. Berg Tag_der_Deutschen_Einheit"):
            sp.events.remove(event)

        # entfernen von KW vor Frau Herzog
        if re.match(r"^\d\d.KW (Fr. Herzog) (.+)", event.name):
            res = re.match(r"^\d\d.KW (Fr. Herzog) (.+)", event.name)
            sp.events[idx].name = res.group(2)
            sp.events[idx].teacher = res.group(1)

        # ersetzen von -Ü am Ende durch Übung am Anfang
        if event.name.endswith("-Ü"):
            sp.events[idx].name = "Übung " + event.name[:-2]

    return sp
