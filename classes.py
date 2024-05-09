from collections import UserDict
import datetime
from datetime import datetime, timedelta
from abc import ABC, abstractmethod



class UserInterface(ABC):

    @abstractmethod
    def send_to_ui(self, message):
        pass

class TerminaUI(UserInterface):

    def send_to_ui(self, message):
        print(f'(Console interface)\n{message}')

class WebUI(UserInterface):

    def send_to_ui(self, message):
        print(f'(Web Interface)\n {message}')


class Field(ABC):
    def __init__(self, value):
        self.value = value
    
    @abstractmethod
    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y").date()
            return True
        except:
            return False
 
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = datetime.strptime(value, "%d.%m.%Y").date()
        else:
            raise ValueError


class Name(Field):
    def is_valid(self, value):
        return bool(value)
                 

class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()
       

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None
    
    def remove_phone(self, phone):
        ph = self.find_phone(phone)
        self.phones.remove(ph)

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p.value) for p in self.phones)}, birthday: {str(self.birthday)} \n"

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        curent_date = datetime.today().date()
        birthdays = []
        for record in self.data.values():
            birthday_date = str(curent_date.year) + str(record.birthday)[4::]
            birthday_date = datetime.strptime(birthday_date,"%Y-%m-%d").date()
            week_day_bdate = birthday_date.isoweekday()
            days_between = (birthday_date - curent_date).days
            if 0 <= days_between < 7:
                match week_day_bdate:
                    case 6:
                        birthdays.append({'name': record.name.value,
                                          'congratulation_date': (birthday_date + timedelta(days=2)).strftime(
                                              "%d.%m.%Y")})
                    case 7:
                        birthdays.append({'name': record.name.value,
                                          'congratulation_date': (birthday_date + timedelta(days=1)).strftime(
                                              "%d.%m.%Y")})
                    case _:
                        birthdays.append(
                            {'name': record.name.value, 'congratulation_date': birthday_date.strftime("%d.%m.%Y")})

        return birthdays

    def __str__(self):
       return f"Contacts: \n{''.join(str(record) for record in self.data.values())}"
