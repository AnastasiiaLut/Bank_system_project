from bank_account import BankAccount, AccountFrozenError, InvalidOperationError, InsufficientFundsError, AccountFrozenError, AccountClosedError, InvalidOperationError

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, min_balance=100, monthly_rate=0.01, 
                 currency="RUB", account_id=None, status="активный"):
        super().__init__(owner, balance, currency, account_id, status)
        self.monthly_rate = monthly_rate
        self.min_balance = min_balance 
    def apply_monthly_interest(self):
        if self.status != "активный":
            raise AccountFrozenError("Ошибка! Счет неактивен.")
        if self._balance<self.min_balance: 
            raise InvalidOperationError(f"Ошибка! Минимальный баланс должен быть больше {self.min_balance}")
        interest = self._balance * self.monthly_rate
        self._balance += interest
        return interest
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
        if self._balance-amount>=self.min_balance:
            self._balance-=amount
            return self._balance
        else:
            raise InvalidOperationError(f"Ошибка! Минимальный баланс должен быть больше {self.min_balance}")    
    def get_account_info(self):
        return f'''{super().get_account_info()}. Минимальный остаток: {self.min_balance}. Месячная ставка доходности: {self.monthly_rate}''' 
    def __str__(self):
        return f'{self.get_account_info()}'
    
    
class PremiumAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_flag=False, increased_limit=50_000, comission=0.1, overdraft_limit=20_000,
                 currency="RUB", account_id=None, status="активный"):
        super().__init__(owner, balance, currency, account_id, status)
        self.increased_limit = increased_limit
        self.comission = comission   
        self.overdraft_flag = overdraft_flag
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.status=="замороженный":
            raise AccountFrozenError('Операция невозможна. Счет заморожен')
        if self.status=="закрытый":
            raise AccountClosedError('Операция невозможна. Счет закрыт')
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError('Операция невозможна. Сумма для снятия должна быть представлена числовым значением')  
        if amount<=0:
            raise InvalidOperationError('Операция невозможна. Сумма должна быть больше нуля') 
            
        total_amount=amount
        
        if amount>self.increased_limit: #Если сумма снятия выше лимита-включаем комиссию
            total_amount=amount*(1+self.comission)
        if self._balance>=total_amount: #Если Баланса на карте хватает
            self._balance -= total_amount
            return (f" Снято {total_amount} {self.currency}. Остаток: {self._balance} {self.currency}")
        elif  self.overdraft_flag==False: # Если не хватило денег на балансе с учетом комиссии и овердрафт не включен
                raise InsufficientFundsError('Недостаточно средств для снятия с учетом комиссии. Для снятия необходимой суммы включите овердрафт.')
        elif  self.overdraft_flag==True: # Если не хватило денег на балансе с учетом комиссии, но овердрафт включен
                if self._balance-total_amount>=-self.overdraft_limit: # Если овердрафта хватило
                    self._balance -= total_amount
                    return (f" Снято {total_amount} {self.currency}. Комиссия составила {amount*self.comission} {self.currency}. Остаток: {self._balance} {self.currency}")      
                else:
                    raise InsufficientFundsError(
                        f"Превышен лимит овердрафта! Доступно с учётом овердрафта: "
                        f"{self._balance + self.overdraft_limit} {self.currency}, запрошено: {total_amount} {self.currency}")
                    
                

    def get_account_info(self):
        base_info = super().get_account_info()
        return (f"{base_info}. Овердрафт: {self.overdraft_limit} {self.currency}. "
                f"Комиссия: {self.comission*100} %.")

    def __str__(self):
        return (f" Премиальный счёт {self.account_id} (владелец: {self.owner}, "
                f"баланс: {self._balance} {self.currency}, овердрафт: {self.overdraft_limit})")
        
class InvestmentAccount(BankAccount):
    def __init__(self, owner, balance, currency="RUB", account_id=None, status="активный"):
        super().__init__(owner, balance, currency, account_id, status)
        self.portfolio = {
            "stocks": [{"name": "",
                       "quantity": 1,
                       "price": 1}],   
            "bonds": [{"name": "",
                       "quantity": 2,
                       "price": 2}],    
            "etf": [{"name": "",
                       "quantity": 3,
                       "price": 3}]     
        }

    class InvestmentAccount(BankAccount):
    def __init__(self, owner, balance, currency="RUB", account_id=None, status="активный"):
        super().__init__(owner, balance, currency, account_id, status)
        self.portfolio = {
            "stocks": [{"name": "",
                       "quantity": 1,
                       "price": 1}],   
            "bonds": [{"name": "",
                       "quantity": 2,
                       "price": 2}],    
            "etf": [{"name": "",
                       "quantity": 3,
                       "price": 3}]     
        }

    def withdraw(self, type_investment, quantity, name):
        if self.status=="замороженный":
            raise AccountFrozenError('Операция невозможна. Счет заморожен')
        if self.status=="закрытый":
            raise AccountClosedError('Операция невозможна. Счет закрыт')
        if not isinstance(quantity, (int, float)):
            raise InvalidOperationError('Операция невозможна. Количество должно быть представлено числовым значением')  
        if quantity<=0:
            raise InvalidOperationError('Операция невозможна. Количество должно быть больше нуля') 
        if type_investment not in ['stocks','bonds','etf']:
            raise InvalidOperationError(f'Операция невозможна.  Используйте: stocks,bonds,etf') 
            
        if name not in [i['name'] for i in  self.portfolio[type_investment]]:
             raise InvalidOperationError(f'Операция невозможна.  Данной инвестиции нет в вашем портфеле') 
            
        if quantity > self.portfolio[type_investment][self.portfolio[type_investment].index([i for i in  self.portfolio[type_investment] if i['name']==name][0])]["quantity"]:
            raise InvalidOperationError(f'Операция невозможна.  Доступное количество: {self.portfolio[type_investment][self.portfolio[type_investment].index([i for i in  self.portfolio[type_investment] if i['name']==name][0])]["quantity"]}, Запрошено: {quantity}') 
        
        

        total_amount=quantity*self.portfolio[type_investment][self.portfolio[type_investment].index([i for i in  self.portfolio[type_investment] if i['name']==name][0])]["price"]
        self._balance+=total_amount
        self.portfolio[type_investment][self.portfolio[type_investment].index([i for i in  self.portfolio[type_investment] if i['name']==name][0])]["quantity"]-=quantity
    
    def project_yearly_growth(self, growth_rates:list):
        
        projected_stocks = sum(i['quantity'] * i['price'] for i in self.portfolio['stocks']) * growth_rates[0]
        projected_bonds = sum(i['quantity']*i['price'] for i in self.portfolio['bonds'])*growth_rates[1]
        projected_etf = sum(i['quantity']*i['price'] for i in self.portfolio['etf'])*growth_rates[2]
        
        total_value = self._balance+projected_stocks+projected_bonds+projected_etf
        
        print(f"📊 Прогнозируемая стоимость портфеля через год (приблизительно): {total_value:.2f} {self.currency}")
        return total_value

    def get_account_info(self):

        base_info = super().get_account_info()
        return (f"{base_info}. Суммарная стоимость акций : {sum([i['price']*i['quantity'] for i in self.portfolio['stocks']])}."
                f"Суммарная стоимость облигаций : {sum([i['price']*i['quantity'] for i in self.portfolio['bonds']])}."
                f"Суммарная стоимость ETF : {sum([i['price']*i['quantity'] for i in self.portfolio['etf']])}.")
    
    def __str__(self):
        return (f"📊 Инвестиционный счёт {self.account_id} (владелец: {self.owner}, "
                f"баланс: {self._balance} {self.currency})")      



