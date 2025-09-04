import yfinance as yf
import pandas as pd

def get_financials(ticker):
    """
    Fetch income statement, balance sheet and cashflow from Yahoo Finance
    Returns: (income_statement, balance_sheet, cashflow)
    """
    stock = yf.Ticker(ticker)
    income_stmt = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T
    return income_stmt, balance_sheet, cashflow

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info