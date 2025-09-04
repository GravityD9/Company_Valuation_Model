import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dcf_model import forecast_fcf, calculate_dcf
from fetch_data import get_financials, get_stock_info
from comparables_model import get_peer_multiples
from visualize import plot_valuation_results
from utils import calculate_wacc
import numpy as np

# --- Step 1: Fetch Company Data ---
ticker = "INFY.NS"
info, income_statement, balance_sheet, cashflow = get_financials(ticker)

print(f"\nCompany: {info['longName']}")
print(f"Market Cap: {info['marketCap']}\n")

print("Income Statement Sample:")
print(income_statement.head())
print()

# --- Step 2: Handle CAPEX column dynamically ---
capex_col = None
for col in cashflow.columns:
    if "Capex" in col or "Capital" in col:
        capex_col = col
        break

if capex_col:
    print(f"⚡ Using CAPEX column: {capex_col}")
    capex = cashflow[capex_col].iloc[0]
else:
    print("⚠️ Warning: No CAPEX column found in cashflow data, using 0 as fallback.")
    capex = 0

# --- Step 3: Forecast Free Cash Flows (DCF) ---
revenue = income_statement["Total Revenue"].iloc[0]
growth_rate = 0.08  # assumed 8% growth
fcf = forecast_fcf(revenue, growth_rate, years=5)

dcf_value = calculate_dcf(fcf, wacc=0.10, terminal_growth=0.03)

print("\n--- Discounted Cash Flow (DCF) Valuation ---")
print("Forecasted Free Cash Flows (next 5 years):", fcf)
print("DCF Valuation: ₹", round(dcf_value, 2))

# --- Step 4: Comparables Valuation ---
pe_val, ev_ebitda_val = get_peer_multiples(ticker)

print("\n--- Comparable Multiples Valuation ---")
print("P/E Multiple Valuation: ₹", round(pe_val, 2))
print("EV/EBITDA Valuation:   ₹", round(ev_ebitda_val, 2))

# --- Step 5: Weighted Average Cost of Capital ---
wacc = calculate_wacc()
print("\n--- Weighted Average Cost of Capital (WACC) ---")
print("Estimated WACC:", round(wacc * 100, 2), "%")

# --- Step 6: Final Valuation Range ---
valuation_range = (min(dcf_value, pe_val, ev_ebitda_val),
                   max(dcf_value, pe_val, ev_ebitda_val))

print(f"\nFinal Valuation Range: ₹ {round(valuation_range[0], 2)} – ₹ {round(valuation_range[1], 2)}")
print("Market Cap (Current): ₹", info["marketCap"])

# --- Step 7: Plot Results ---
plot_valuation_results(dcf_value, pe_val, ev_ebitda_val, info["marketCap"])
