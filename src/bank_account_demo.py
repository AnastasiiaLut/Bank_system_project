from bank_account import BankAccount, AccountFrozenError

active_account = BankAccount('Иванов Иван', 1000, status="активный")
frozen_account = BankAccount('Петров Петр', 2000, status="замороженный")

# 1. Создание активного и замороженного счета
print("Активный счёт:", active_account.get_account_info())
print("Замороженный счёт:", frozen_account.get_account_info())
print()

# 2. Попытка операции над замороженным счётом (вылетит ошибка)
print("Пытаемся снять 500 с замороженного счёта")
try:
    frozen_account.withdraw(500)
except AccountFrozenError as e:
    print(f"Ошибка: {e}")
print()

# 3. Валидное пополнение активного счёта
print("Пополняем активный счёт на 500")
active_account.deposit(500)
print("После пополнения:", active_account.get_account_info())
print()

# 4. Валидное снятие с активного счёта
print("Снимаем 100 с активного счёта")
active_account.withdraw(100)
print("После снятия:", active_account.get_account_info())
