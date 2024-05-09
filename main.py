from classes import AddressBook, Record, UserInterface, TerminaUI, WebUI
import pickle


class Commander:
    @classmethod
    def run(cls, source):
        if source == 'console':
            ui = TerminaUI()
        elif source == 'web':
            ui = WebUI()
        else:
            print('Unknown source: %s' % source)
        main(ui)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not exist"
        except IndexError:
            return "Contact not found"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday)
    return f'Birthday {birthday} to contact {name} added'


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = f'Contact {name} update successfully'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f'Contact {name} added successfully'
    if phone:
        record.add_phone(phone)
    return message


@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f'Contact {name} not found'
    record.edit_phone(old_phone, new_phone)
    return f'Contact {name} successfully changed'


def exit(args, book: AddressBook):
    return 'Good bye!'


def hello(args, book: AddressBook):
    return 'How can I help you?'


def show_all(args, book: AddressBook):
    return book


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return f'Contact {name} not found'
    return record.birthday


@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if not record:
        return f'Contact {name} not found'
    return '; '.join(str(phone) for phone in record.phones)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 
    

def main(ui: UserInterface):
    commands = {
        'add': add_contact,
        'add-birthday': add_birthday,
        'all': show_all,
        'birthdays': birthdays,
        'change': change_contact,
        'hello': hello,
        'phone': show_phone,
        'show-birthday': show_birthday, 
    }
    book = load_data('addressbook.pkl')
    ui.send_to_ui('Welcome to the assistant bot!')
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            ui.send_to_ui('Good by!')
            save_data(book)
            break
        elif command in ['?', 'help']:
            ui.send_to_ui(f'Available commands: {", ".join(commands.keys())}')
        else:
            try:
                ui.send_to_ui(commands[command](args, book))
            except KeyError:
                ui.send_to_ui('Invalid command.')


if __name__ == "__main__":
    Commander.run('console')
