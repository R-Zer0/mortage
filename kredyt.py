import numpy as np
from prettytable import PrettyTable

# Параметры кредита
principal = 490000  # Основной долг
annual_interest_rate = 7.61 / 100  # Годовая процентная ставка
monthly_interest_rate = annual_interest_rate / 12  # Месячная процентная ставка
term_5_years = 5 * 12  # Количество месяцев для первых 5 лет
term_15_years = 15 * 12  # Общее количество месяцев для 15 лет
additional_payment = 0  # Дополнительные платежи (если есть)
additional_payment_start_month = 12  # Месяц начала дополнительных платежей
insurance_total = 13238.86  # Общая сумма страхования

# Расчет ежемесячного платежа
monthly_payment = (principal + insurance_total) * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_15_years) / ((1 + monthly_interest_rate) ** term_15_years - 1)
monthly_insurance_payment = insurance_total / term_5_years

print(f'Ежемесячная выплата: {monthly_payment:.2f} PLN')
print(f'Ежемесячная доплата: {additional_payment:.2f} PLN')

# Инициализация остатка по кредиту и суммарных платежей
remaining_principal = principal
total_paid = 0
total_interest_paid = 0

# Подготовка таблицы для вывода
table = PrettyTable()
table.field_names = ["Month", "Rate fixed", "Principal", "Interest", "Remaining", "Additional"]
table.float_format = '.2'

# Процесс платежей и досрочных погашений
for month in range(1, term_15_years + 1):
    if remaining_principal <= 0:
        break

    interest_payment = remaining_principal * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment

    # Учитываем страховые выплаты первые 5 лет
    if month <= term_5_years:
        principal_payment -= monthly_insurance_payment

    additional_payment_this_month = 0
    if month > additional_payment_start_month:
        additional_payment_this_month = additional_payment

    remaining_principal -= principal_payment + additional_payment_this_month
    total_paid += monthly_payment + additional_payment_this_month
    total_interest_paid += interest_payment

    table.add_row([month, monthly_payment, principal_payment, interest_payment, remaining_principal, additional_payment_this_month])

print(table)

# Итоговые результаты
print(f'Общая сумма выплат за 15 лет: {total_paid:.2f} PLN')
print(f'Общая сумма выплаченных процентов: {total_interest_paid:.2f} PLN')
print(f'Переплата: {total_paid - principal:.2f} PLN')
