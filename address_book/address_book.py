import operator
from collections import UserDict
from datetime import datetime

from .fields import Birthday
from .record import Record


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.get_name()] = record

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def __str__(self):
        return "Contacts:\n" + '; \n'.join(str(contact) for contact in self.data.values())

    def get_upcoming_birthdays(self) -> list:
        """Find users who have a birthday in the next 7 days"""

        result = []

        for record in self.data.values():
            if not type(record.birthday) == Birthday:
                continue

            today = datetime.today()

            current_year = today.year
            year_diff = current_year - record.birthday.value.year
            # find the nearest next birthday
            next_birthday = record.birthday.value.replace(year=record.birthday.value.year + year_diff).date()
            if next_birthday < today.date():
                next_birthday = next_birthday.replace(year=next_birthday.year + 1)

            birthday_diff = next_birthday - today.date()
            # skip user if the birthday is more than 7 days away
            if birthday_diff.days > 7:
                continue

            # if the birthday is on a day off, postpone the date to the next Monday
            if next_birthday.weekday() > 4:
                next_birthday = next_birthday.replace(day=next_birthday.day + 7 - next_birthday.weekday())

            result.append({"name": record.name.value, "congratulation_date": next_birthday.strftime("%Y.%m.%d")})

        # Sort result list by birthday date
        return sorted(result, key=operator.itemgetter('congratulation_date'))
