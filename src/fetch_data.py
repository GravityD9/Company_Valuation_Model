import yfinance as yf
import pandas as pd

def get_financials(ticker):
    """
    Fetches company info, income statement, balance sheet, and cashflow.
    Normalizes column names to avoid mismatches.
    """
    stock = yf.Ticker(ticker)

    info = stock.info

    income_statement = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T

    # --- Normalize column names ---
    def normalize_columns(df):
        df.columns = (
            df.columns.str.strip()
                      .str.replace(" ", "_")
                      .str.replace("-", "_")
                      .str.replace("(", "")
                      .str.replace(")", "")
                      .str.lower()
        )
        return df

    income_statement = normalize_columns(income_statement)
    balance_sheet = normalize_columns(balance_sheet)
    cashflow = normalize_columns(cashflow)

    return info, income_statement, balance_sheet, cashflow


def get_stock_info(ticker):
    """Fetches basic stock information"""
    stock = yf.Ticker(ticker)
    return stock.info
