import re

import requests
from bs4 import BeautifulSoup

from configs.url_config import ROI_URL


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

    @ticker.getter
    def ticker(self, new_ticker):
        self._ticker = new_ticker.upper()

    @property
    def roic(self):
        url = ROI_URL.format(ticker=self._ticker, company=self._company)
        soup = self._get_soup(url)
        table = soup.find_all(text=re.compile('Return on Investment Historical Data'))[0].parent.parent.parent.parent
        return table

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

    def _get_soup(self, url):
        r = requests.get(url)
        r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html)
        return soup