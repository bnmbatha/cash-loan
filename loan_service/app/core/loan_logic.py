# Function to calculate the monthly loan repayment amount
def calculate_monthly_payment(amount: float, term: int, interest_rate: float) -> float:
    # Convert the annual interest rate to a monthly rate
    # For example, 12% annual becomes 0.01 (1%) monthly
    monthly_rate = interest_rate / 100 / 12

    # If there is no interest rate, return a simple division
    if monthly_rate == 0:
        return amount / term  # Divide the loan amount equally over the term

    # Calculate the monthly repayment using the amortization formula:
    # M = P * r / (1 - (1 + r)^-n)
    # Where:
    # M = monthly payment
    # P = loan amount
    # r = monthly interest rate
    # n = total number of months
    return round((amount * monthly_rate) / (1 - (1 + monthly_rate) ** -term), 2)
