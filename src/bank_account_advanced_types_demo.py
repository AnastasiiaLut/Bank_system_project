# Создаём сберегательный счёт
savings = SavingsAccount("Анна", 1000, min_balance=200, monthly_rate=0.015, currency="USD")

print("=== ИНФОРМАЦИЯ ===")
print(savings.get_account_info())
print()

# 1. Начисление процентов (баланс 1000 >= 200)
print("1. Начисление процентов:")
savings.apply_monthly_interest()
print(savings.get_account_info())

# 2. Снятие допустимой суммы (останется 500 >= 200)
print("2. Снятие 300 USD:")
savings.withdraw(300)
print(savings.get_account_info())

# 3. Снятие, которое сделает остаток меньше минимума (200)
print("3. Снятие 700 USD (останется 15 < 200):")
try:
    savings.withdraw(700)
    print(savings.get_account_info())
except InvalidOperationError as e:
    print(e)
print()

# 4. Снятие с недостатком средств (превышает баланс)
print("4. Снятие 2000 USD (больше баланса):")
try:
    savings.withdraw(2000)
except InsufficientFundsError as e:
    print(e)
print()

# 5. Создаём замороженный счёт и пытаемся начислить проценты
frozen_savings = SavingsAccount("Борис", 500, min_balance=100, status="замороженный")
print("5. Попытка начисления процентов на замороженном счёте:")
try:
    frozen_savings.apply_monthly_interest()
except AccountFrozenError as e:
    print(e)
print()

# 6. Вывод строкового представления
print("6. __str__:")
print(savings)



# Пример использования PremiumAccount 

# Создаём премиальный счёт с овердрафтом
premium = PremiumAccount(
    owner="Екатерина",
    balance=60_000,
    overdraft_flag=True,          # овердрафт разрешён
    increased_limit=15_000,       # лимит без комиссии 15 000
    comission=0.15,              # комиссия 15% за превышение лимита
    overdraft_limit=5_000,        # можно уйти в минус до -5 000
    currency="RUB"
)

# Выводим информацию о счете
print("=== ИНФОРМАЦИЯ О СЧЁТЕ ===")
print(premium.get_account_info())
print()

# 1. Снимаем сумму меньше лимита (комиссии нет)
print("1. Снятие 10 000 RUB (менее лимита 15 000):")
result = premium.withdraw(10_000)
print(result)
print(f"Баланс после: {premium._balance} RUB\n")

# 2. Снимаем сумму больше лимита, но денег хватает с комиссией
print("2. Снятие 20 000 RUB (превышает лимит, комиссия 15%):")
result = premium.withdraw(20_000)
print(result)
print(f"Баланс после: {premium._balance} RUB\n")

# 3. Снимаем сумму, при которой подключается овердрафт (денег не хватает)
print("3. Снятие 29 000 RUB (баланс 27 000, не хватает 3 000, овердрафт покрывает):")
try:
    result = premium.withdraw(27_500)
    print(result, '\n')
except InsufficientFundsError as e:
    print(e, '\n')
    
# 4. Попытка снять больше, чем позволяет овердрафт (ошибка)
print("4. Попытка снять 10 000 RUB (превышает лимит овердрафта):")
try:
    premium.withdraw(10_000)
except InsufficientFundsError as e:
    print(e,"\n")

# 5. Строковое представление счёта
print("5. Строковое представление:")
print(premium)


# 1. Создаём инвестиционный счёт с начальным балансом 10 000 RUB
investor = InvestmentAccount("Елена Смирнова", 10000, currency="RUB")

# 2. Выводим детальную информацию о счете (стоимости активов)
print("=== ИНФОРМАЦИЯ О СЧЁТЕ ===")
print(investor.get_account_info())
# Ожидаемый вывод:
# Суммарная стоимость акций : 1.0.Суммарная стоимость облигаций : 4.0.Суммарная стоимость ETF : 9.0.

# 3. Прогнозируем рост портфеля через год.
# Предположим: акции вырастут на 12%, облигации на 5%, ETF на 8%.
growth_rates = [0.12, 0.05, 0.08]
print("\n=== ПРОГНОЗ РОСТА ===")
future_value = investor.project_yearly_growth(growth_rates)
# Расчёт:
# Текущая стоимость акций: 1 * 1 = 1 → прирост 0.12
# Текущая стоимость облигаций: 2 * 2 = 4 → прирост 0.20 (4 * 0.05)
# Текущая стоимость ETF: 3 * 3 = 9 → прирост 0.72 (9 * 0.08)
# Прогнозируемая стоимость = 10000 + 0.12 + 0.20 + 0.72 = 10001.04 RUB
# Вывод:  Прогнозируемая стоимость портфеля через год (приблизительно): 10001.04 RUB

# 4. Выводим строковое представление счёта (метод __str__)
print("\n=== СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ ===")
print(investor)