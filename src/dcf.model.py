import numpy as np

def forecast_fcf(net_income, capex, depreciation, change_in_wc, years=5, growth_rate=0.05):
    """
    Simple FCF forecast = Net Income + Depreciation - Capex - Change in WC
    Growth rate applied each year
    """
    fcf = []
    base = net_income + depreciation - capex - change_in_wc
    for i in range(years):
        fcf.append(base * ((1 + growth_rate) ** (i+1)))
    return fcf

def calculate_dcf(fcf, wacc, terminal_growth):
    """
    DCF valuation using Gordon Growth for terminal value
    """
    projection_years = len(fcf)
    discount_factors = [(1 + wacc) ** i for i in range(1, projection_years+1)]
    discounted_fcfs = [fcf[i] / discount_factors[i] for i in range(projection_years)]

    terminal_value = fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    terminal_value_discounted = terminal_value / ((1 + wacc) ** projection_years)

    enterprise_value = sum(discounted_fcfs) + terminal_value_discounted
    return enterprise_value
