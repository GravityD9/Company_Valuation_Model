import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dcf_model import forecast_fcf, calculate_dcf
from fetch_data import get_financials, get_stock_info
from comparables_model import get_peer_multiples
from visualize import plot_valuation_results
from utils import calculate_wacc
import numpy as np


if __name__ == "__main__":
    # Example: Infosys
    ticker = "INFY.NS"
    income_stmt, balance_sheet, cashflow = get_financials(ticker)
    info = get_stock_info(ticker)

    print("Company:", info.get("shortName"))
    print("Market Cap:", info.get("marketCap"))
    print("\nIncome Statement Sample:\n", income_stmt.head())

    # Example inputs for DCF
    net_income = income_stmt["Net Income"].iloc[0]
    capex = cashflow["Capital Expenditures"].iloc[0]
    depreciation = cashflow["Depreciation"].iloc[0]
    change_in_wc = 0  # Simplified assumption

    fcf_forecast = forecast_fcf(net_income, capex, depreciation, change_in_wc, years=5, growth_rate=0.06)
    wacc = calculate_wacc()
    terminal_growth = 0.03

    dcf_value = calculate_dcf(fcf_forecast, wacc, terminal_growth)
    print(f"\nDCF Enterprise Value: {dcf_value:,.2f}")

    # Comparables valuation
    peers = ["TCS.NS", "WIPRO.NS", "HCLTECH.NS"]
    peer_multiples = get_peer_multiples(peers)
    print("\nPeer Multiples:", peer_multiples)

    # Aggregate results
    results = {
        "DCF": dcf_value,
        "Peer Avg (P/E)": np.nanmean([v["P/E"] for v in peer_multiples.values() if v["P/E"]]),
        "Peer Avg (EV/EBITDA)": np.nanmean([v["EV/EBITDA"] for v in peer_multiples.values() if v["EV/EBITDA"]])
    }

    plot_valuation_results(results)
