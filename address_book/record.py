from .fields import Name, Birthday, Phone


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
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, to_find_phone):
        for phone in self.phones:
            if phone.value == to_find_phone:
                return phone

        return None

    def get_name(self):
        return self.name.value

    def __str__(self):
        contact_str = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if not self.birthday is None:
            contact_str += f", birthday {self.birthday.value}"

        return contact_str
