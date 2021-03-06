import datetime
import constants
import calendar


def show_menu():
    """Shows menu"""
    message = """\nChoose an option
1 - Show current funds
2 - Expenses per month
3 - Exit from the program\n"""
    print(message)


def input_datetime(message):
    """Returns time string or requests input from user again"""
    while True:
        user_input = input(message)
        try:
            datetime.datetime.strptime(user_input, "%m-%Y")
            return user_input
        except ValueError:
            print("Incorrect format. Use MM-YYYY")


def get_bank_name(phone):
    """Returns bank name
    If bank was not found returns False"""
    if phone in constants.banks:
        return constants.banks[phone]
    else:
        return False


def read_data(dataset):
    """read dataset file
 replace all newline symbols
 separate phone number, time and text
 add items to list"""
    data = list()
    read_only = 'r'
    with open(dataset, read_only) as file:
        for line in file:
            transaction = dict()
            line = line.replace('\n', '').split(';')
            line[2] = line[2].split(' ')
            transaction['phone'] = line[0]
            transaction['time'] = line[1]
            transaction['text'] = line[2]
            data.append(transaction)
    return data


def get_expenses_per_month(data, date):
    """Returns total expenses for specific month
    Returns nested list
    First list consisting of two integer numbers specifies card numbers
    Second list consisting of two integer numbers specifies total expences
    Third list consisting of two integer numbers specifies total incomes
    First number in each list always stores SuperBank
    Second number in each list always stores GorgeousBank
    [[c1,c2],[ex1,ex2],[in1,in2]]"""
    records = []
    total_expenses = [0, 0]
    total_incomes = [0, 0]
    card_numbers = [0, 0]
    year = int(date[1])
    month = int(date[0])
    days_in_month = calendar.monthrange(year, month)[1]
    date = datetime.datetime(year, month, 1)
    begin = date.replace(day=1, hour=00, minute=00, second=00, microsecond=0)
    end = date.replace(day=days_in_month, hour=23, minute=59, second=59, microsecond=0)
    for item in data:
        date = item['time'].split(' ')[0].split('-')
        year = int(date[2])
        month = int(date[1])
        date = datetime.datetime(year, month, 1)
        if date <= end and date >= begin:
            records.append(item)
            phone = item['phone']
            bank_name = get_bank_name(phone)
            if bank_name == constants.banks['480']:
                card_numbers[0] = item['text'][1]
                if item['text'][0] == 'Withdrawal':
                    total_expenses[0] += int(item['text'][2])
                else:
                    total_incomes[0] += int(item['text'][2])
            else:
                 card_numbers[1] = item['text'][0]
                 sum_of_transaction = int(item['text'][1])
                 if sum_of_transaction < 0:
                    total_expenses[1] += abs(int(item['text'][1]))
                 else:
                     total_incomes[1] += int(item['text'][1])
    if card_numbers[0] != 0 or card_numbers[1] != 0:
        return [card_numbers, total_expenses, total_incomes, records]
    else:
        return 0


def get_my_cards(data):
    cards = set()
    for item in data:
        if item['phone'] == '480':
            cards.add(item['text'][1])
        else:
            cards.add(item['text'][0])
    return cards


def get_current_funds(data, phone):
    latest_date = datetime.datetime(1, 1, 1, 00, 00, 00)
    current_message = 0
    for message in data:
        if message['phone'] == phone:
            time = message['time']
            time = time.split(' ')
            time[0] = time[0].split('-')
            time[1] = time[1].split(':')
            date = datetime.datetime(int(time[0][2]), int(time[0][1]), int(time[0][0]), int(time[1][0]), int(time[1][1]), int(time[1][2]))
            if date > latest_date:
                latest_date = date
                current_message = message
    if phone == '480':
        return current_message['text'][3]
    else:
        return current_message['text'][2]


