from abc import ABC, abstractmethod
import uuid

class AbstractAccount(ABC):
    def __init__(self, account_id, owner, balance, status='активный'):
        self.account_id=account_id
        self.owner=owner
        self._balance=balance 
        self.status=status
        
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_account_info(self):
        pass


class BankAccountRaw(AbstractAccount):
    currencies = ["RUB", "USD", "EUR", "KZT", "CNY"]
    statuses = ["активный", "замороженный", "закрытый"]
    def __init__(self, owner, balance, currency="RUB", account_id=None, status="активный"):

        if type(balance)!=int and type(balance)!=float:
            raise ValueError("Недопустимое значение. Значение баланса должно быть представлено числовым значением")
            
        if balance < 0:
            raise ValueError("Недопустимое значение. Начальный баланс должен быть положительным")
            
        if currency not in BankAccount.currencies:
            raise ValueError(f"Недопустимое значение. Используйте: {self.currencies}")
        
        if status not in BankAccount.statuses:
            raise ValueError(f"Недопустимое значение. Используйте: {self.statuses}")

        if not account_id:
            account_id = f"{str(uuid.uuid4())[:8]}"

        super().__init__(account_id, owner, balance, status)
        self.currency = currency

class AccountFrozenError(Exception):
    pass

class AccountClosedError(Exception):
    pass

class InvalidOperationError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass  

class BankAccount(BankAccountRaw):
    def deposit(self, amount):
        if self.status=="замороженный":
            raise AccountFrozenError('Операция невозможна. Счет заморожен')
        if self.status=="закрытый":
            raise AccountClosedError('Операция невозможна. Счет закрыт')
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError('Операция невозможна. Сумма для снятия должна быть представлена числовым значением')  
        if amount<=0:
            raise InvalidOperationError('Операция невозможна. Сумма должна быть больше нуля')    
        self._balance+=amount

    def withdraw(self, amount):
        if self.status=="замороженный":
            raise AccountFrozenError('Операция невозможна. Счет заморожен')
        if self.status=="закрытый":
            raise AccountClosedError('Операция невозможна. Счет закрыт')
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError('Операция невозможна. Сумма для снятия должна быть представлена числовым значением')  
        if amount<=0:
            raise InvalidOperationError('Операция невозможна. Сумма должна быть больше нуля')    
        if self._balance<amount:
            raise InsufficientFundsError('Недостаточно средств')    
        self._balance-=amount
    def get_account_info(self):
        return f'''Счёт: {self.account_id}, Владелец: {self.owner}, Баланс: {self._balance}, Статус: {self.status}, Валюта:{self.currency}'''
    def __str__(self):
        return f'{self.get_account_info()}'    
            