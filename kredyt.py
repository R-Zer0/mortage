from prettytable import PrettyTable

def calculate_annuity_loan(principal, annual_interest_rate, term_months, insurance_total, additional_payment=0, additional_payment_start_month=0):
    monthly_interest_rate = annual_interest_rate / 12

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
            insurance_payment = insurance_total / (5 * 12)
            principal_payment -= insurance_payment

        # Ensure principal payment is not negative
        if principal_payment < 0:
            principal_payment = 0

        additional_payment_this_month = 0

        # Make additional payment to match differentiated payment, avoiding negative additional payments
        if month > additional_payment_start_month:
            additional_payment_this_month = additional_payment

        remaining_principal -= principal_payment + additional_payment_this_month
        total_paid += monthly_payment + additional_payment_this_month
        total_interest_paid += interest_payment

        annuity_data.append([month, monthly_payment, principal_payment, interest_payment, max(0, remaining_principal), additional_payment_this_month])

    return annuity_data, total_paid, total_interest_paid

# Main parameters
principal = 490000
annual_interest_rate = 7.71 / 100
term_years = 15
term_months = term_years * 12
insurance_total = 13238.86
additional_payment = 0
additional_payment_start_month = 12

# Calculate annuity loan
annuity_data, annuity_total_paid, annuity_total_interest_paid = calculate_annuity_loan(
    principal, annual_interest_rate, term_months, insurance_total, additional_payment, additional_payment_start_month
)

# Prepare table for output
table = PrettyTable()
table.field_names = ["Month", "Payment", "Principal", "Interest", "Remaining", "Additional"]
table.float_format = '.2'

# Fill table with data
for annuity_row in annuity_data:
    table.add_row(annuity_row)

print(table)

# Final results
print(f'Annuity Loan - Total payments over {term_years} years: {annuity_total_paid:.2f} PLN')
print(f'Annuity Loan - Total interest paid: {annuity_total_interest_paid:.2f} PLN')
print(f'Annuity Loan - Overpayment: {annuity_total_paid - principal:.2f} PLN')
