import numpy as np
from prettytable import PrettyTable

def calculate_annuity_loan(principal, annual_interest_rate, term_years, monthly_insurance_payment):
    monthly_interest_rate = annual_interest_rate / 12
    term_months = term_years * 12
    
    # Расчет ежемесячного платежа для аннуитетного кредита
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / ((1 + monthly_interest_rate) ** term_months - 1)
    
    remaining_principal = principal
    total_paid = 0
    total_interest_paid = 0
    
    annuity_data = []
    
    for month in range(1, term_months + 1):
        if remaining_principal <= 0:
            break
        
        interest_payment = remaining_principal * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment

        # Учитываем страховые выплаты только первые 5 лет
        if month <= 5 * 12:
            principal_payment -= monthly_insurance_payment

        additional_payment_this_month = 0

        # Делаем переплату, чтобы сравнять с дифференцированным платежом, но не позволяя отрицательные доплаты
        if principal_payment + interest_payment < (principal / term_months + interest_payment):
            additional_payment_this_month = (principal / term_months + interest_payment) - principal_payment - interest_payment

        remaining_principal -= principal_payment + additional_payment_this_month
        total_paid += monthly_payment + additional_payment_this_month
        total_interest_paid += interest_payment

        annuity_data.append([month, monthly_payment, principal_payment, interest_payment, max(0, remaining_principal), additional_payment_this_month])
    
    return annuity_data, total_paid, total_interest_paid

def calculate_differentiated_loan(principal, annual_interest_rate, term_years, monthly_insurance_payment):
    monthly_interest_rate = annual_interest_rate / 12
    term_months = term_years * 12
    
    monthly_principal_payment = principal / term_months

    
    remaining_principal = principal
    total_paid = 0
    total_interest_paid = 0
    
    differentiated_data = []
    
    for month in range(1, term_months + 1):
        interest_payment = remaining_principal * monthly_interest_rate
        monthly_payment = monthly_principal_payment + interest_payment

        # Учитываем страховые выплаты только первые 5 лет
        if month <= 5 * 12:
            monthly_payment += monthly_insurance_payment
        
        remaining_principal -= monthly_principal_payment
        total_paid += monthly_payment
        total_interest_paid += interest_payment

        differentiated_data.append([month, monthly_payment, monthly_principal_payment, interest_payment, max(0, remaining_principal)])
    
    return differentiated_data, total_paid, total_interest_paid

# Основные параметры
principal = 490000
annual_interest_rate = 7.61 / 100
term_years = 15
insurance_total = 13238.86
monthly_insurance_payment = insurance_total / (5 * 12) if insurance_total else 0  # Страховка только первые 5 лет

# Расчет аннуитетного кредита
annuity_data, annuity_total_paid, annuity_total_interest_paid = calculate_annuity_loan(
    principal, annual_interest_rate, term_years, monthly_insurance_payment
)

# Расчет дифференцированного кредита
differentiated_data, differentiated_total_paid, differentiated_total_interest_paid = calculate_differentiated_loan(
    principal, annual_interest_rate, term_years, monthly_insurance_payment
)

# Подготовка таблицы для вывода
table = PrettyTable()
table.field_names = ["Month", "Annuity Payment", "Annuity Principal", "Annuity Interest", "Annuity Remaining",
                     "Differentiated Payment", "Differentiated Principal", "Differentiated Interest", "Differentiated Remaining", "Additional"]
table.float_format = '.2'

# Определяем количество месяцев для вывода
max_months = max(len(annuity_data), len(differentiated_data))

# Заполнение таблицы данными
for i in range(max_months):
    annuity_row = annuity_data[i] if i < len(annuity_data) else [0] * len(annuity_data[0])
    differentiated_row = differentiated_data[i] if i < len(differentiated_data) else [0] * len(differentiated_data[0])
    
    combined_row = [i+1] + annuity_row[1:5] + differentiated_row[1:5] + [annuity_row[5]]
    table.add_row(combined_row)

print(table)

# Итоговые результаты
print(f'Аннуитетный кредит - Общая сумма выплат за {term_years} лет: {annuity_total_paid:.2f} PLN')
print(f'Аннуитетный кредит - Общая сумма выплаченных процентов: {annuity_total_interest_paid:.2f} PLN')
print(f'Аннуитетный кредит - Переплата: {annuity_total_paid - principal:.2f} PLN')

print(f'Дифференцированный кредит - Общая сумма выплат за {term_years} лет: {differentiated_total_paid:.2f} PLN')
print(f'Дифференцированный кредит - Общая сумма выплаченных процентов: {differentiated_total_interest_paid:.2f} PLN')
print(f'Дифференцированный кредит - Переплата: {differentiated_total_paid - principal:.2f} PLN')
