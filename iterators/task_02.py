from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        return (elem for sublist in ((period[0] + timedelta(days=i) for i in range((period[1]-period[0]).days + 1)) for period in self.dates) for elem in sublist)


dates = [(datetime(2020, 1, 1), datetime(2020, 1, 7)), (datetime(2020, 1, 15), datetime(2020, 2, 7))]
m = Movie('sw', dates)

for d in m.schedule():
    print(d)

for period in dates:
    for date in [period[0] + timedelta(days=i) for i in range((period[1]-period[0]).days + 1)]:
        print(date)

for date in (elem for sublist in ((period[0] + timedelta(days=i) for i in range((period[1]-period[0]).days + 1)) for period in dates) for elem in sublist):
    print(date)

(elem for sublist in ((period[0] + timedelta(days=i) for i in range((period[1]-period[0]).days + 1)) for period in dates) for elem in sublist)
