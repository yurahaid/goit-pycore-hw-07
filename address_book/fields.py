import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
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
