def calculate_monthly_payment(amount: float, term: int, interest_rate: float) -> float:
    monthly_rate = interest_rate / 100 / 12
    if monthly_rate == 0:
        return amount / months    
    return round((amount * monthly_rate) / (1 - (1 + monthly_rate) ** -months), 2)
