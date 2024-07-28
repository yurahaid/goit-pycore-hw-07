import operator
import re
from collections import UserDict
from datetime import datetime
from functools import cmp_to_key


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone must contains only 10 digits")
        super().__init__(value)

    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            input_format = "%d.%m.%Y"
            input_datetime = datetime.strptime(value, input_format)
            super().__init__(input_datetime)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == old_phone:
                self.phones[i] = Phone(new_phone)

                return

    def find_phone(self, to_find_phone):
        for phone in self.phones:
            if phone.value == to_find_phone:
                return phone

        return None

    def get_name(self):
        return self.name.value

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.get_name()] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

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
        return  sorted(result, key=operator.itemgetter('congratulation_date'))

