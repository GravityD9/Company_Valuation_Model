def calculate_wacc(cost_of_equity=0.12, cost_of_debt=0.08, equity_value=0.7, debt_value=0.3, tax_rate=0.25):
    """
    Weighted Average Cost of Capital
    """
    wacc = (equity_value * cost_of_equity) + (debt_value * cost_of_debt * (1 - tax_rate))
    return wacc