import yfinance as yf

def get_peer_multiples(peers=None):
    if peers is None:
        peers = ["INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS"]

    pe_ratios = []
    ev_ebitdas = []

    for peer in peers:
        stock = yf.Ticker(peer)
        info = stock.fast_info

        pe = info.get("trailing_pe", None)
        enterprise_value = info.get("enterprise_value", None)
        ebitda = info.get("ebitda", None)

        if pe:
            pe_ratios.append(pe)
        if enterprise_value and ebitda and ebitda != 0:
            ev_ebitdas.append(enterprise_value / ebitda)

    # Average multiples
    avg_pe = sum(pe_ratios) / len(pe_ratios) if pe_ratios else 0
    avg_ev_ebitda = sum(ev_ebitdas) / len(ev_ebitdas) if ev_ebitdas else 0

    return avg_pe, avg_ev_ebitda
