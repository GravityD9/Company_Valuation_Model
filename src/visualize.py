import matplotlib.pyplot as plt

def plot_valuation_results(dcf_value, pe_valuation, ev_ebitda_valuation, market_cap):
    """
    Plots a comparative bar chart of company valuation metrics.
    
    Parameters:
        dcf_value (float): Discounted Cash Flow valuation
        pe_valuation (float): P/E Multiple valuation
        ev_ebitda_valuation (float): EV/EBITDA Multiple valuation
        market_cap (float): Current Market Capitalization
    """
    labels = ['DCF', 'P/E', 'EV/EBITDA', 'Market Cap']
    values = [dcf_value, pe_valuation, ev_ebitda_valuation, market_cap]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])
    
    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'₹ {yval:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.title("Company Valuation Comparison", fontsize=14)
    plt.ylabel("₹ Value", fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.show()


# --- Optional test ---
if __name__ == "__main__":
    plot_valuation_results(3.19e11, 0, 0, 6.06e12)
