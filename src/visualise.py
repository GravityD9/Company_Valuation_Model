import matplotlib.pyplot as plt

def plot_valuation_results(results_dict):
    """
    Plot bar chart of valuation results
    results_dict: {"DCF": value, "Peer Avg (P/E)": value, "Peer Avg (EV/EBITDA)": value}
    """
    names = list(results_dict.keys())
    values = list(results_dict.values())

    plt.figure(figsize=(8,5))
    plt.bar(names, values, color=["skyblue","lightgreen","salmon"])
    plt.title("Valuation Results")
    plt.ylabel("Value (in Cr / $ depending on data)")
    plt.show()
