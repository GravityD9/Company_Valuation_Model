import yfinance as yf
import pandas as pd

def get_peer_multiples(peers=None):
    if peers is None:
        peers = ["INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS"]

    pe_ratios = []
    ev_ebitdas = []

    for peer in peers:
        stock = yf.Ticker(peer)

        try:
            info = stock.fast_info
            pe = info.get("trailing_pe", None)
            enterprise_value = info.get("enterprise_value", None)
            ebitda = info.get("ebitda", None)

            # --- Debug prints ---
            print(f"DEBUG {peer} - fast_info PE: {pe}, EV: {enterprise_value}, EBITDA: {ebitda}")

            # Use fast_info if available
            if pe and pe > 0:
                pe_ratios.append(pe)
            if enterprise_value and ebitda and ebitda != 0:
                ev_ebitdas.append(enterprise_value / ebitda)

            # --- Fallback: compute manually if missing ---
            fin = stock.financials
            bs = stock.balance_sheet

            # Manual PE calculation
            if not pe or pe <= 0:
                try:
                    net_income = None
                    if "Net Income" in fin.index:
                        net_income = fin.loc["Net Income"].iloc[0]
                    elif "NetIncome" in fin.index:
                        net_income = fin.loc["NetIncome"].iloc[0]

                    market_cap = info.get("market_cap", None)
                    if market_cap and net_income and net_income != 0:
                        pe_manual = market_cap / net_income
                        pe_ratios.append(pe_manual)
                        print(f"DEBUG {peer} - Manual PE: {pe_manual:.2f}")
                except Exception as e:
                    print(f"DEBUG {peer} - Manual PE calculation failed: {e}")

            # Manual EV/EBITDA calculation
            if not ev_ebitdas or len(ev_ebitdas) == 0:
                try:
                    ebitda_val = None
                    if "EBITDA" in fin.index:
                        ebitda_val = fin.loc["EBITDA"].iloc[0]
                    elif "Ebitda" in fin.index:
                        ebitda_val = fin.loc["Ebitda"].iloc[0]

                    total_debt = bs.loc["Total Debt"].iloc[0] if "Total Debt" in bs.index else 0
                    cash = bs.loc["Cash And Cash Equivalents"].iloc[0] if "Cash And Cash Equivalents" in bs.index else 0

                    market_cap = info.get("market_cap", None)
                    if market_cap and ebitda_val and ebitda_val != 0:
                        ev = market_cap + total_debt - cash
                        ev_ebitdas.append(ev / ebitda_val)
                        print(f"DEBUG {peer} - Manual EV/EBITDA: {ev/ebitda_val:.2f}")
                except Exception as e:
                    print(f"DEBUG {peer} - Manual EV/EBITDA calculation failed: {e}")

        except Exception as e:
            print(f"⚠️ Skipping {peer} due to error: {e}")

    # --- Compute average multiples ---
    avg_pe = sum(pe_ratios) / len(pe_ratios) if pe_ratios else 0
    avg_ev_ebitda = sum(ev_ebitdas) / len(ev_ebitdas) if ev_ebitdas else 0

    return avg_pe, avg_ev_ebitda


# --- Test ---
if __name__ == "__main__":
    pe, ev_ebitda = get_peer_multiples()
    print(f"Peer Avg PE: {pe:.2f}x, Peer Avg EV/EBITDA: {ev_ebitda:.2f}x")
