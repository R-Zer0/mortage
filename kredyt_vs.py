from prettytable import PrettyTable

def calculate_annuity_loan(principal, annual_interest_rate, term_years, monthly_insurance_payment):
    monthly_interest_rate = annual_interest_rate / 12
    term_months = term_years * 12

    # Calculate monthly payment for annuity loan
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

        # Consider insurance payments only for the first 5 years
        if month <= 5 * 12:
            principal_payment -= monthly_insurance_payment

        # Ensure principal payment is not negative
        if principal_payment < 0:
            principal_payment = 0

        additional_payment_this_month = 0

        # Make additional payment to match differentiated payment, avoiding negative additional payments
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

        # Consider insurance payments only for the first 5 years
        if month <= 5 * 12:
            monthly_payment += monthly_insurance_payment

        remaining_principal -= monthly_principal_payment
        total_paid += monthly_payment
        total_interest_paid += interest_payment

        differentiated_data.append([month, monthly_payment, monthly_principal_payment, interest_payment, max(0, remaining_principal)])

    return differentiated_data, total_paid, total_interest_paid

# Main parameters
principal = 490000
annual_interest_rate = 7.61 / 100
term_years = 15
insurance_total = 13238.86
monthly_insurance_payment = insurance_total / (5 * 12) if insurance_total else 0  # Insurance only for the first 5 years

# Calculate annuity loan
annuity_data, annuity_total_paid, annuity_total_interest_paid = calculate_annuity_loan(
    principal, annual_interest_rate, term_years, monthly_insurance_payment
)

# Calculate differentiated loan
differentiated_data, differentiated_total_paid, differentiated_total_interest_paid = calculate_differentiated_loan(
    principal, annual_interest_rate, term_years, monthly_insurance_payment
)

# Prepare table for output
table = PrettyTable()
table.field_names = ["Month", "An. Payment", "An. Principal", "An. Interest", "An. Remaining",
                     "Dif. Payment", "Dif. Principal", "Dif. Interest", "Dif. Remaining", "Additional"]
table.float_format = '.2'

# Determine the number of months for output
max_months = max(len(annuity_data), len(differentiated_data))

# Fill table with data
for i in range(max_months):
    annuity_row = annuity_data[i] if i < len(annuity_data) else [0] * len(annuity_data[0])
    differentiated_row = differentiated_data[i] if i < len(differentiated_data) else [0] * len(differentiated_data[0])

    combined_row = [i+1] + annuity_row[1:5] + differentiated_row[1:5] + [annuity_row[5]]
    table.add_row(combined_row)

print(table)

# Final results
print(f'Annuity Loan - Total payments over {term_years} years: {annuity_total_paid:.2f} PLN')
print(f'Annuity Loan - Total interest paid: {annuity_total_interest_paid:.2f} PLN')
print(f'Annuity Loan - Overpayment: {annuity_total_paid - principal:.2f} PLN')

print(f'Differentiated Loan - Total payments over {term_years} years: {differentiated_total_paid:.2f} PLN')
print(f'Differentiated Loan - Total interest paid: {differentiated_total_interest_paid:.2f} PLN')
print(f'Differentiated Loan - Overpayment: {differentiated_total_paid - principal:.2f} PLN')