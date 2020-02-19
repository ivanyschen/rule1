import re

import requests
from bs4 import BeautifulSoup

from configs.scraper_config import *


class RuleOne:

    def __init__(self, company=None, ticker=None):
        self._company = company.lower().replace(' ', '-')
        self._ticker = ticker.upper()

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, new_company):
        self._company = new_company.lower().replace(' ', '-')

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, new_ticker):
        self._ticker = new_ticker.upper()

    @property
    def roic(self):
        url = ROI_URL.format(ticker=self._ticker, company=self._company)
        soup = get_soup(url)
        data = get_annual_roic(soup)
        return data

    @property
    def equity(self):
        pass

    @property
    def equity_growth(self):
        pass

    @property
    def eps(self):
        pass

    @property
    def eps_growth(self):
        pass

    @property
    def revenue(self):
        pass

    @property
    def revenue_growth(self):
        pass

    @property
    def cash(self):
        pass

    @property
    def cash_growth(self):
        pass

    def _compute_growth(self):
        pass

def get_soup(url):
    r = requests.get(url)
    r.raise_for_status()
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_data_rows(soup, table):
    table = soup.find_all(text=re.compile(table))[0].parent.parent.parent.parent
    table_rows = [ele for ele in table.find('tbody').find_all('tr')]
    return table_rows

def get_annual_roic(soup, table=ROIC_TABLE):
    table_rows = get_data_rows(soup, table)
    data = []
    for row in table_rows:
        date, _, _, roic = [td.text for td in row.find_all('td')]
        data.append((date, roic))
    return data

def get_annual_revenue(soup, table=REVENUE_TABLE):
    table_rows = get_data_rows(soup, table)
    data = []
    for row in table_rows:
        date, revenue = [td.text for td in row.find_all('td')]
        data.append((date, revenue))
    return data

def get_annual_cash(soup, table=CASH_TABLE):
    table_rows = get_data_rows(soup, table)
    data = []
    for row in table_rows:
        date, cash = [td.text for td in row.find_all('td')]
        data.append((date, cash))
    return data

def get_annual_equity(soup, table=EQUITY_TABLE):
    table_rows = get_data_rows(soup, table)
    data = []
    for row in table_rows:
        date, cash = [td.text for td in row.find_all('td')]
        data.append((date, cash))
    return data

def get_annual_eps(soup, table=EPS_TABLE):
    table_rows = get_data_rows(soup, table)
    data = []
    for row in table_rows:
        date, cash = [td.text for td in row.find_all('td')]
        data.append((date, cash))
    return data

