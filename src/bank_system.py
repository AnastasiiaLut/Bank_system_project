from bank_account import BankAccount, AccountFrozenError, InvalidOperationError, InsufficientFundsError,  AccountClosedError

from bank_account_advanced_types import SavingsAccount, PremiumAccount, InvestmentAccount

import datetime

class Client():
    def __init__(self, full_name, client_id, client_status='активный', account_numbers_list:list=None, contacts:list=None, age=0, pin=123):
        if age<18:
            raise ValueError('Извините, мы не обслуживаем лиц, не достигших 18 лет')
        else:
            self.age=age
            
        self.full_name=full_name
        self.client_id=client_id
        self.client_status=client_status
        
        if  account_numbers_list==None:
            self.account_numbers_list = []
        else:
            self.account_numbers_list = account_numbers_list

        if  contacts==None:
            self.contacts = []
        else:
            self.contacts = contacts
            
        self.__pin=pin
        self.failed_attempts = 0
            
        self.suspicious_actions:list = [] # Здесь можно оставить [] так как эта строка находится в теле метода, а не в переменных функции

        self.accounts_ids = []

    def check_pin(self, pin):
        if self.__pin==pin:
            return True
        else:
            return False



class Bank():
    def __init__(self, 
                 clients_dict=None): # {client_id: client} 
        if  clients_dict==None:
            self.clients_dict = {}
        else:
            self.clients_dict = clients_dict
        self.accounts = {} # {account_id: account (то есть там объект счета)}
        

        
    def add_client(self, new_client):
        if datetime.time(hour=0)<=datetime.datetime.now().time()<=datetime.time(hour=5):
            new_client.suspicious_actions.append('Попытка добавления нового клиета с 00:00 до 05:00')
            raise InvalidOperationError('Действуют ограничения на данный тип операций с 00:00 до 05:00')
            
        if new_client.client_id in self.clients_dict:
            raise KeyError('Данный аккаунт уже существует')
        else:
            self.clients_dict[new_client.client_id]=new_client
        return 'Спасибо, что выбрали нас!'
        
    def open_account(self, account_type, client, **kwargs):

        account_classes = {
            'standard': BankAccount,
            'savings': SavingsAccount,
            'premium': PremiumAccount,
            'investment': InvestmentAccount
        }
        if account_type not in account_classes:
            raise InvalidOperationError(f"Неизвестный тип счёта: {account_type}")


        account = account_classes[account_type](**kwargs)

        self.accounts[account.account_id] = account     


        client.accounts_ids.append(account.account_id)

        return account.account_id
        
    def close_account(self, client, account_id):
        if datetime.time(hour=0)<=datetime.datetime.now().time()<=datetime.time(hour=5):
            client.suspicious_actions.append('Попытка закрытия аккаунта клиета с 00:00 до 05:00')
            raise InvalidOperationError('Действуют ограничения на данный тип операций с 00:00 до 05:00')
        self.accounts[account_id].status='закрытый'
        return 'Аккаунт закрыт'   
        

        
    def freeze_account(self, client, account_id):
        if datetime.time(hour=0)<=datetime.datetime.now().time()<=datetime.time(hour=5):
            client.suspicious_actions.append('Попытка заморозки аккаунта клиета с 00:00 до 05:00')
            raise InvalidOperationError('Действуют ограничения на данный тип операций с 00:00 до 05:00')
        self.accounts[account_id].status='замороженный'
        return 'Аккаунт заморожен'

    
        
    def unfreeze_account(self, client, account_id):
        if datetime.time(hour=0)<=datetime.datetime.now().time()<=datetime.time(hour=5):
            client.suspicious_actions.append('Попытка разморозки аккаунта клиета с 00:00 до 05:00')
            raise InvalidOperationError('Действуют ограничения на данный тип операций с 00:00 до 05:00')
        self.accounts[account_id].status='активный'
        return 'Аккаунт разморожен'
        

    def authenticate_client(self, client, pin_in):
        while client.failed_attempts<3:
            if not client.check_pin(pin_in):
                client.failed_attempts+=1
                client.suspicious_actions.append('Введен неверный пароль')
                raise ValueError(f'Неверный пароль. Осталось попыток: {3-client.failed_attempts}')
            else:
                client.failed_attempts=0
                return print(f'Здравствуйте!')
        client.client_status = 'замороженный'      


    def search_accounts(self, account_id):
        if account_id not in self.accounts:
            raise ValueError('Данный счет не найден')
        else:
            return(self.accounts[account_id])

    def get_total_balance(self):
        return sum([i._balance for i in self.accounts.values()])


    def get_clients_ranking(self):
        clients_ranking = []
        for i in self.clients_dict:
            clients_ranking.append((i, sum([self.accounts[acc_id]._balance for acc_id in self.clients_dict[i].accounts_ids])))
        return(sorted(clients_ranking, key=lambda x:x[1], reverse=True)) 
