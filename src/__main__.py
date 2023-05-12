"""
The main script
"""

from .automata import EventQueue, PersonState, PersonStateEnum

# Init a person
person = PersonState(EventQueue(), PersonStateEnum.REST)

for day in range(30):
    print(f"Started day {day + 1}")
    for hour in range(24):
        print(f"Day {day + 1}, Hour {hour}:")
        _ = person.next_state(hour)
