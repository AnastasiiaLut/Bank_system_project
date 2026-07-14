from bank_account import BankAccount, AccountFrozenError, InvalidOperationError, InsufficientFundsError,  AccountClosedError

from bank_account_advanced_types import SavingsAccount, PremiumAccount, InvestmentAccount

from bank_system import Client, Bank

# Создаём банк
bank = Bank()

# Создаём клиента 1 (возраст 25, PIN 1234)
client = Client("Иван Петров", "C001", age=25, pin=1234)


# Создаём клиента 2 (возраст 27, PIN 4321)
client2 = Client("Мария Сидорова", "C002", age=27, pin=4321)

# Добавляем клиента в банк
bank.add_client(client)
bank.add_client(client2)

# Открываем стандартный счёт с балансом 5000 RUB
account_id = bank.open_account("standard", client, owner="Иван", balance=5000, currency="RUB")
account_id2 = bank.open_account("standard", client2, owner="Мария", balance=7000, currency="RUB")

# Показываем баланс счёта
print(f"Баланс счёта {account_id}: {bank.accounts[account_id]._balance} RUB")

# Аутентификация клиента (верный PIN)
bank.authenticate_client(client, 1234)

# Замораживаем счёт
bank.freeze_account(client, account_id)
print(f"Статус счёта после заморозки: {bank.accounts[account_id].status}")

# Пытаемся снять деньги с замороженного счёта (ожидаем ошибку)
try:
    bank.accounts[account_id].withdraw(100)
except AccountFrozenError as e:
    print(f"Ошибка при снятии: {e}")

# Размораживаем счёт
bank.unfreeze_account(client, account_id)
print(f"Статус после разморозки: {bank.accounts[account_id].status}")



# Общая сумма всех счетов в банке
print(f"Общая сумма балансов: {bank.get_total_balance()} RUB")

# Рейтинг клиентов (по сумме балансов)
print("Рейтинг клиентов:", bank.get_clients_ranking())


# Снимаем все деньги, чтобы закрыть счёт (баланс должен быть 0)
bank.accounts[account_id].withdraw(5000)

# Показываем баланс счёта
print(f"Баланс счёта {account_id}: {bank.accounts[account_id]._balance} RUB")

# Закрываем счёт
bank.close_account(client, account_id)
print(f"Статус после закрытия: {bank.accounts[account_id].status}")