from collections import UserDict
from datetime import date, datetime


def input_error(in_func):
    def wrapper(*args):
        try:
            check = in_func(*args)
            return check
        except KeyError:
            return 'There is no such a contact. Please try again'
        except IndexError:
            return 'Give me name and phone please'
        except ValueError:
            return 'ValueError'
        except TypeError:
            return 'TypeError'

    return wrapper


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value


class Phone(Field):
    def __init__(self, phone_list):
        self.__phone_list = None
        self.phone_list = phone_list

    @property
    def phone_list(self):
        return self.__phone_list

    @phone_list.setter
    def phone_list(self, phone_list):
        if phone_list.isdigit():
            self.__phone_list = phone_list

    def __repr__(self) -> str:
        return str(self.__phone_list)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, b_date):
        self.__b_date = None
        self.b_date = b_date

    @property
    def b_date(self):
        return self.__b_date

    @b_date.setter
    def b_date(self, b_date):
        try:
            self.__b_date = datetime.strptime(b_date, '%Y-%m-%d').date()
        except ValueError as e:
            return "Birthdate must be in 'dd.mm.yy' format"

    def __repr__(self) -> str:
        return self.b_date.strftime('%Y-%m-%d')


# Record реализует методы для добавления/удаления/редактирования объектов Phone.


class Record:
    def __init__(self, name: Name, phone: Phone = None, b_date: Birthday = None):
        self.name = name
        self.phones = []  # коллекции называем во множественном числе
        if phone:
            self.phones.append(phone)
        self.b_date = b_date

    def add_number_to_record(self, phone: Phone):  # это излишнее наименование)
        self.phones.append(phone)

    def del_number_from_record(self, phone: Phone):
        for i in self.phones:
            if i.phone_list == phone.phone_list:
                self.phones.remove(i)

    def change_number_in_record(self, phone: Phone, phone_new: Phone):
        for i in self.phones:
            if i.phone_list == phone.phone_list:
                self.phones[self.phones.index(i)] = phone_new

    def days_to_birthday(self):
        if self.b_date:
            b_d = self.b_date.b_date
            result = datetime(datetime.now().year, b_d.month, b_d.day) - datetime.now()
            if result.days > 0:
                return result.days
            return "The birthday is over"
        return "Birthdate not set"

    def __repr__(self):
        if self.b_date is None:
            return f'{self.name.value}, {self.phones}'
        else:
            return f'{self.name.value}, {self.phones}, {self.b_date}'


class AddressBook(UserDict):
    counter = 0
    # def __init__(self, counter=1):
    #     # self.data = {}
    #     self.count = 0
    #     self.counter = counter

    def set_pages(self, page):
        self.counter = page

    # def __iter__(self):
    #     self.count = 0
    #     return self
    #
    # def __next__(self):
    #     if self.count > self.counter:
    #         raise StopIteration
    #     else:
    #         self.count += 1
    #         return self.data

    def add_to_addressbook(self, record: Record):
        self.data[record.name.value] = record

    def iterator_addressbook(self, *args):
        self.counter = int(args[0])
        number_of_iterations = int(args[1])
        b = list(dict.keys(self.data))
        while int(self.counter) < number_of_iterations:
            yield self[b[self.counter]]
            self.counter += 1
            if self.counter == number_of_iterations:
                input("press any Enter to continue...")
                number_of_iterations += int(args[1])
                if number_of_iterations > len(b):
                    number_of_iterations = len(b)


def ex(*args):
    return "Good bye!"


@input_error
def add_to_addressbook(addressbook: AddressBook, *args):
    if args[0].isdigit():
        return "The contact name should be in letters"
    tmp_name = Name(args[0])
    tmp_phone1 = Phone(args[1])
    tmp_rec = Record(tmp_name, tmp_phone1)
    addressbook.add_to_addressbook(tmp_rec)
    return f'Contact {tmp_rec.name.value} with phones {tmp_phone1} added successfully'


def show_addressbook(addressbook: AddressBook, *args):
    if args[0] == '':
        for k, v in addressbook.data.items():
            print(f"Name for the contact {k}, phone\\s {v.phones}, birthday is {v.b_date}" if v.b_date else
                  f"Name for the contact {k}, phone\\s {v.phones}, birthday is not defined")
        return 'End of the PhoneBook'
    if args[0].isdigit():
        if int(args[0]) > len(addressbook.data.values()):
            print('Now you will get a whole book')
            for k, v in addressbook.data.items():
                print(f"Name for the contact {k}, phone\\s {v.phones}, birthday is {v.b_date}" if v.b_date else
                      f"Name for the contact {k}, phone\\s {v.phones}, birthday is not defined")
            return 'End of the PhoneBook'
        if int(args[0]) <= len(addressbook.data.values()):
            by_steps = addressbook.iterator_addressbook(addressbook.counter, args[0])
            for rec in by_steps:
                print(rec)
            addressbook.counter = 0
        return "End of the Addressbook"


@input_error
def find_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            return k, v.phones


@input_error
def add_phone_to_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            add_num = Phone(args[1])
            Record.add_number_to_record(v, add_num)
            return f'Number {add_num.phone_list} was added'


@input_error
def erase_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            del_num = Phone(args[1])
            Record.del_number_from_record(v, del_num)
            return f'Number {del_num.phone_list} was deleted'


def change_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            ch_num_in = Phone(args[1])
            ch_num_for = Phone(args[2])
            Record.change_number_in_record(v, ch_num_in, ch_num_for)
            return f'Number {ch_num_in.phone_list} was changed to {ch_num_for.phone_list}'


def check_contact_b_day(addressbook: AddressBook, *args):
    rec = addressbook.data.get(args[0])
    if rec:
        return rec.days_to_birthday()


def helps(*args):
    print('You can use following commands:')
    print('"show", "s" - to show the whole PhoneBook')
    print('"add" - to add the contact to the Phone book \\ example: add ContactName Phone \\+ Phone....')
    print('"ap" - add phone for existing contact \\ example: ap NameOfExistingContact Phone \\+ Phone....')
    print('"change", "ch" - to update existing phone number for contact \\ example: change '
          'NameOfExistingContact Phone \\+ Phone....')
    print('"erase" - to erase existing phone for the contact \\ example: erase NameOfExistingContact '
          'Phone \\+ Phone....')
    print('"birthday", "bdate", "bd" - to check how many days till next birthday for the contact '
          '\\ example: ch NameOfExistingContact')
    print('"exit", ".", "bye" - for exit')
    return 'make your choice'


COMMANDS = {ex: ["exit", ".", "bye"], show_addressbook: ["show", "s"], add_to_addressbook: ["add"],
            find_contact: ["find", "f"], add_phone_to_contact: ["ap"], erase_phone: ["erase"],
            change_phone: ["change", "ch"], check_contact_b_day: ["birthday", "bdate", "bd"], helps: ["help", "h"],}


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")


def main():
    print('Welcome to the worst PhoneBook EVER')
    print('type "help" or "h" to receive a help')
    phone_book = AddressBook()
    name1 = Name('Alberto')
    name2 = Name('Dell')
    name3 = Name('Rio')
    name4 = Name('Antony')
    phone1 = Phone('3232323')
    phone2 = Phone('6666664')
    phone3 = Phone('23432423')
    phone4 = Phone('23123123')
    bdate1 = Birthday('1990-05-18')
    bdate2 = Birthday('1980-07-09')

    r = Record(name1, phone1, bdate1)  # если хотите реализовать множественную передачу одинаковых данных, возьмите их в кортеж) но сейчас лучше по одному
    r.add_number_to_record(phone3)
    r2 = Record(name2, phone2)
    r3 = Record(name3, phone3, bdate2)
    r4 = Record(name4, phone4)
    r3.add_number_to_record(phone2)

    phone_book.add_to_addressbook(r)  # в объектах Record уже есть имя, потому это лишняя передача.
    phone_book.add_to_addressbook(r2)
    phone_book.add_to_addressbook(r3)
    phone_book.add_to_addressbook(r4)
    while True:
        tmp = input('Please input command: ')
        result, data = parse_command(tmp)
        print(result(phone_book, *data))
        if result is ex:
            break


if '__main__' == __name__:
    main()
