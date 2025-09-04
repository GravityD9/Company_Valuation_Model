import yfinance as yf

def get_peer_multiples(tickers):
    multiples = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe_ratio = info.get("trailingPE", None)
        ev_ebitda = info.get("enterpriseToEbitda", None)
        multiples[ticker] = {"P/E": pe_ratio, "EV/EBITDA": ev_ebitda}
    return multiples
