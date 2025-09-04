import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dcf_model import forecast_fcf, calculate_dcf
from fetch_data import get_financials, get_stock_info
from comparables_model import get_peer_multiples
from visualize import plot_valuation_results
from utils import calculate_wacc
import numpy as np

# --- Helper function for safe column lookup ---
def safe_get(df, keywords, default=0):
    """
    Returns the first matching column in df for any of the given keywords.
    If not found, returns default value.
    """
    for col in df.columns:
        for kw in keywords:
            if kw in col:
                return df[col].iloc[0]
    print(f"⚠️ Warning: none of {keywords} found in DataFrame. Using default {default}")
    return default

# --- Step 1: Fetch Company Data ---
ticker = "INFY.NS"
info, income_statement, balance_sheet, cashflow = get_financials(ticker)

# --- DEBUG: Show available cashflow columns ---
print("Available Cashflow Columns:")
print(cashflow.columns.tolist())
print("==================================================\n")

print("\n================ COMPANY OVERVIEW ================")
print(f"Company: {info.get('longName', 'N/A')}")
print(f"Market Cap: ₹ {info.get('marketCap', 0):,.0f}")

print("\n--- Income Statement Sample ---")
print(income_statement.head())
print("==================================================\n")

# --- Step 2: Extract Key Financials ---
revenue = safe_get(income_statement, ["total_revenue", "operating_revenue"])
capex = safe_get(cashflow, ["capital_expenditures"])
ebit = safe_get(income_statement, ["ebit", "operating_income"])
net_income = safe_get(income_statement, ["net_income"])

print("Key Metrics (Most Recent Year):")
print(f"   Total Revenue:       ₹ {revenue:,.0f}")
print(f"   EBIT:                ₹ {ebit:,.0f}")
print(f"   Net Income:          ₹ {net_income:,.0f}")
print(f"   Capital Expenditures: ₹ {capex:,.0f}")
print("==================================================\n")

# --- Step 3: Forecast Free Cash Flows (DCF) ---
growth_rate = 0.08  # assumed 8% growth

# --- Extract Depreciation & Working Capital ---
depreciation = safe_get(cashflow, ["depreciation", "depreciation_and_amortization"])
change_in_wc = safe_get(cashflow, ["change_in_working_capital", "changes_in_working_capital"])

print(f"Depreciation & Amortization: ₹ {depreciation:,.0f}")
print(f"Change in Working Capital:   ₹ {change_in_wc:,.0f}")

fcf = forecast_fcf(revenue, growth_rate, depreciation, change_in_wc, years=5)
dcf_value = calculate_dcf(fcf, wacc=0.10, terminal_growth=0.03)

print("--- Discounted Cash Flow (DCF) Valuation ---")
print("Forecasted Free Cash Flows (₹):", [f"{x:,.0f}" for x in fcf])
print(f"DCF Valuation: ₹ {dcf_value:,.0f}")
print("==================================================\n")

# --- Step 4: Comparable Multiples Valuation ---
avg_pe, avg_ev_ebitda = get_peer_multiples()

# Infosys Net Income & EBITDA (from financials)
net_income = safe_get(income_statement, ["net_income"])
ebitda = safe_get(income_statement, ["ebitda", "normalized_ebitda"])

# Infosys Enterprise Value = Market Cap + Debt - Cash
market_cap = info.get("marketCap", 0)
total_debt = safe_get(balance_sheet, ["total_debt"], default=0)
cash = safe_get(balance_sheet, ["cash"], default=0)
enterprise_value = market_cap + total_debt - cash

# Apply multiples
pe_valuation = net_income * avg_pe
ev_ebitda_valuation = ebitda * avg_ev_ebitda

print("--- Comparable Multiples Valuation ---")
print(f"Peer Avg P/E Multiple:       {avg_pe:.2f}x")
print(f"Peer Avg EV/EBITDA Multiple: {avg_ev_ebitda:.2f}x")
print(f"P/E Multiple Valuation:      ₹ {pe_valuation:,.0f}")
print(f"EV/EBITDA Valuation:         ₹ {ev_ebitda_valuation:,.0f}")
print("==================================================\n")

# --- Step 5: Weighted Average Cost of Capital ---
wacc = calculate_wacc()
print("--- Weighted Average Cost of Capital ---")
print(f"Estimated WACC: {wacc * 100:.2f}%")
print("==================================================\n")

# --- Step 6: Final Valuation Range ---
valuation_range = (min(dcf_value, pe_val, ev_ebitda_val),
                   max(dcf_value, pe_val, ev_ebitda_val))

print("--- Final Valuation Summary ---")
print(f"Valuation Range: ₹ {valuation_range[0]:,.0f} – ₹ {valuation_range[1]:,.0f}")
print(f"Current Market Cap: ₹ {info.get('marketCap', 0):,.0f}")
print("==================================================\n")

# --- Step 7: Plot Results ---
plot_valuation_results(dcf_value, pe_val, ev_ebitda_val, info["marketCap"])