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
    pass


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
    def __init__(self, value):
        self.value = value


class Birthday(Field):
    def __init__(self, b_date):
        self.__b_date = None
        self.b_date = b_date

    @property
    def b_date(self):
        return self.__b_date

    @b_date.setter
    def b_date(self, b_date): # сдесь нужно реализовать парсер и помещать в в виде datetime объекта
        try:
            self.__b_date = datetime.strptime(b_date, '%Y-%m-%d').date()
        except ValueError as e:
            return "Birtdate must be in 'dd.mm.yy' format"
        # if len(b_date) == 10:
        #     self.__b_date = b_date
    
    def __repr__(self) -> str:
        return self.b_date.strftime('%Y-%m-%d')


# Record реализует методы для добавления/удаления/редактирования объектов Phone.


class Record:
    def __init__(self, name:Name, phone:Phone=None, b_date:Birthday=None): # плохой стиль написания( или все в args, или именованные
        self.name = name
        self.phones = [] #коллекции называем во множественном числе
        if phone:
            self.phones.append(phone)
        self.b_date = b_date

    def add_number_to_record(self, phone: Phone): # это излишнее наименование)
        self.phones.append(phone)

    def del_number_from_record(self, phone: Phone):
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)

    def change_number_in_record(self, phone: Phone, phone_new: Phone):
        for i in self.phones:
            if i.value == phone.value:
                self.phones[self.phones.index(i)] = phone_new

    def days_to_birthday(self): # , b_day: Birthday = None дата дня рождения уже есть в объектк
        # Да - полет фантазии - огонь)
        
        if self.b_date:
            b_d = self.b_date.b_date
            result = datetime(datetime.now().year, b_d.month, b_d.day) - datetime.now()
            if result.days > 0:
                return result.days
            return "The birthday is over"
        return "Birthdate not set"
        
        
        # current_datetime = datetime.now()
        # birthday_data = b_day.b_date
        # birthday_data_strip = birthday_data.split("-")
        # if int(birthday_data_strip[1]) < current_datetime.month:
        #     birthday_data_string = datetime(year=current_datetime.year + 1, month=int(
        #         birthday_data_strip[1]), day=int(birthday_data_strip[2]) + 1)
        #     return (birthday_data_string - current_datetime).days
        # elif int(birthday_data_strip[1]) == current_datetime.month:
        #     birthday_data_string = datetime(year=current_datetime.year, month=int(
        #         birthday_data_strip[1]), day=int(birthday_data_strip[2]) + 1)
        #     if birthday_data_string < current_datetime:
        #         birthday_data_string = datetime(year=current_datetime.year + 1, month=int(
        #             birthday_data_strip[1]), day=int(birthday_data_strip[2]) + 1)
        #         return (birthday_data_string - current_datetime).days
        #     else:
        #         return (birthday_data_string - current_datetime).days
        # else:
        #     birthday_data_string = datetime(year=current_datetime.year, month=int(
        #         birthday_data_strip[1]), day=int(birthday_data_strip[2]))
        #     return (birthday_data_string - current_datetime).days


class AddressBook(UserDict):
    counter = 2
    # def __init__(self, counter=None):
    #     self.data = {}
    #     self.count = 0
    #     self.counter = counter
    def set_pages(self, page):
        self.counter = page

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count > self.counter:
            raise StopIteration
        else:
            self.count += 1
            return self.data

    def add_to_addressbook(self,record: Record):
        self.data[record.name.value] = record


def ex(*args):
    return "Good bye!"


class CustomIterator:
    def __init__(self, counter=1):
        self.counter = counter

    def __iter__(self):
        return AddressBook(self)


# превращаю список телефонов в кортеж обьектов Phone
@input_error
def parse_phones(raw__p: list):
    tmp_p_list = []
    for i in raw__p:
        tmp_p = Phone(i)
        tmp_p_list.append(tmp_p)
    return tuple(tmp_p_list)


@input_error
def add_to_addressbook(addressbook: AddressBook, *args):
    if args[0].isdigit():
        return "The contact name should be in letters"
    tmp_name = Name(args[0])
    tmp_phone1 = parse_phones(args[1:])
    tmp_rec = Record(tmp_name, tmp_phone1)
    addressbook.add_to_addressbook(tmp_name, tmp_rec)
    return f'Contact {tmp_rec.name.value} with phones {tmp_phone1} added successfully'


def show_addressbook(addressbook: AddressBook, *args):
    if args[0] == '':
        for k, v in addressbook.data.items():
            print(k, v.phones, v.b_date if v.b_date else '')
    if args[0].isdigit():
        # show_book = CustomIterator()
        
        for contacts in addressbook:
            print(contacts)
        # show_book = addressbook
        # for contacts in show_book:
        #     print(contacts)
        return "Please input numbers of showing contacts"

    # showing_phone_book = {}
    # for k, v in addressbook.data.items():
    #     if isinstance(Birthday, v):
    #
    #     if type(v.phone[0]) == tuple:
    #         v.phone = list(v.phone[0])
    #     phones = ', '.join([str(i.value) for i in v.phone])
    #     showing_phone_book[k] = phones
    # return showing_phone_book


@input_error
def find_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            return k, v.phone


@input_error
def add_phone_to_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            add_num = Phone(args[1])
            Record.add_number_to_record(v, add_num)
            return f'Number {add_num.value} was added'


@input_error
def erase_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            del_num = Phone(args[1])
            Record.del_number_from_record(v, del_num)
            return f'Number {del_num.value} was deleted'


def change_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            ch_num_in = Phone(args[1])
            ch_num_for = Phone(args[2])
            Record.change_number_in_record(v, ch_num_in, ch_num_for)
            return f'Number {ch_num_in.value} was changed to {ch_num_for.value}'


def check_contact_b_day(addressbook: AddressBook, *args): # Нужно просто принять ключ, имя контакта и вернуть дни до его ДР
    rec = addressbook.data.get(args[0])
    if rec:
        return rec.days_to_birthday()
    return f'Addresbook dont have contact with name {args[0]}'
            # if isinstance(v.phone[-1], Birthday):
            #     b_day = v.phone[-1
            #     return Record.days_to_birthday(v, b_day)
            # else:
            #     return f'Contact {args[0]} doesnt have a birthday field'


COMMANDS = {ex: ["exit", ".", "bye"], show_addressbook: ["show", "s"], add_to_addressbook: ["add"],
            find_contact: ["find", "f"], add_phone_to_contact: ["ap"], erase_phone: ["erase"],
            change_phone: ["change", "ch"], check_contact_b_day: ["birthday", "bdate", "bd"]}


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")


def main():
    print('Welcome to the worst PhoneBook EVER')
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
    print("==================================================")
    phone_book = AddressBook()
    name1 = Name('Alberto')
    name2 = Name('Dell')
    name3 = Name('Rio')

    phone1 = Phone('3232323')
    phone2 = Phone('6666664')
    phone3 = Phone('23432423')

    bdate1 = Birthday('1990-05-18')
    bdate2 = Birthday('1980-07-09')

    r = Record(name1, phone1, bdate1) # если хотите реализовать множественную передачу одинаковых данных, возьмите их в кортеж) но сейчас лучше по одному
    r.add_number_to_record(phone3)
    r2 = Record(name2, phone2)
    r3 = Record(name3, phone3, bdate2)
    r3.add_number_to_record(phone2)

    phone_book.add_to_addressbook(r) # в объектах Record уже есть имя, потому это лишняя передача.
    phone_book.add_to_addressbook(r2)
    phone_book.add_to_addressbook(r3)

    while True:
        tmp = input('Please input command: ')
        result, data = parse_command(tmp)
        print(result(phone_book, *data))
        if result is ex:
            break


if '__main__' == __name__:
    main()
