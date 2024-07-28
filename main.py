from address_book.address_book import AddressBook
from address_book.record import Record


def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{e}"

    return inner
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@handle_error
def add_contact(args, address_book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args

    record = address_book.find(name)
    if record is None:
        record = Record(name)

    record.add_phone(phone)

    address_book.add_record(record)

    return "Contact added."

@handle_error
def change_contact(args, address_book: AddressBook):
    if len(args) != 3:
        raise ValueError("Give me name, phone and old phone please.")

    name, old_phone, new_phone = args

    record = address_book.find(name)
    if record is None:
        raise KeyError(f"Contact with name {name} not found")

    record.edit_phone(old_phone, new_phone)

    return "Contact changed."

@handle_error
def add_birthday(args, address_book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")

    name, birthday = args

    record = address_book.find(name)
    if record is None:
        raise KeyError(f"Contact with name {name} not found")

    record.add_birthday(birthday)

    return "Birthday added."


@handle_error
def show_birthday(args, address_book: AddressBook):
    if len(args) != 1:
        raise ValueError("Give me name")
    name = args[0]

    record = address_book.find(name)
    if record is None:
        raise KeyError(f"Contact with name {name} not found")

    return record.birthday

@handle_error
def phone(args, address_book: AddressBook):
    if len(args) != 1:
        raise ValueError("Give me name")
    name = args[0]

    record = address_book.find(name)
    if record is None:
        raise KeyError(f"Contact with name {name} not found")

    return record.phones


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(book.get_upcoming_birthdays())
        elif command == "all":
            print(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
