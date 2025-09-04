import yfinance as yf

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

            # If fast_info has valid multiples
            if pe and pe > 0:
                pe_ratios.append(pe)
            if enterprise_value and ebitda and ebitda != 0:
                ev_ebitdas.append(enterprise_value / ebitda)

            # --- Fallback: compute manually if missing ---
            if not pe or not ev_ebitdas:
                fin = stock.get_income_stmt(freq="annual")
                bs = stock.get_balance_sheet(freq="annual")

                if not pe:
                    try:
                        net_income = fin.loc["Net Income"].iloc[0]
                        market_cap = info.get("market_cap", None)
                        if market_cap and net_income:
                            pe_ratios.append(market_cap / net_income)
                    except Exception:
                        pass

                if not ev_ebitdas:
                    try:
                        ebitda_val = fin.loc["EBITDA"].iloc[0]
                        total_debt = bs.loc["Total Debt"].iloc[0] if "Total Debt" in bs.index else 0
                        cash = bs.loc["Cash And Cash Equivalents"].iloc[0] if "Cash And Cash Equivalents" in bs.index else 0
                        market_cap = info.get("market_cap", None)
                        if market_cap and ebitda_val and ebitda_val != 0:
                            ev = market_cap + total_debt - cash
                            ev_ebitdas.append(ev / ebitda_val)
                    except Exception:
                        pass

        except Exception as e:
            print(f"⚠️ Skipping {peer} due to error: {e}")

    # --- Average multiples across peers ---
    avg_pe = sum(pe_ratios) / len(pe_ratios) if pe_ratios else 0
    avg_ev_ebitda = sum(ev_ebitdas) / len(ev_ebitdas) if ev_ebitdas else 0

    return avg_pe, avg_ev_ebitda
