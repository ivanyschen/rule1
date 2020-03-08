import re

import requests
from bs4 import BeautifulSoup

from configs.scraper_config import *


class MacroTrendCrawler:

    def _get_soup(self, url):
        r = requests.get(url)
        r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def _get_data_rows(self, soup, table):
        table = soup.find_all(text=re.compile(table))[0].parent.parent.parent.parent
        table_rows = [ele for ele in table.find('tbody').find_all('tr')]
        return table_rows

    def _process_precentage_records(self, annual_records):
        processed_records = []
        for date, percentage in annual_records:
            if percentage[:-1] == 'inf':
                break
            processed_records.append((date, round(float(percentage[:-1]) * 0.01, 4)))
        return processed_records

    def _process_dollar_records(self, annual_records):
        processed_records = []
        for date, money in annual_records:
            money = money[1:]
            if not money:
                break
            money = money.replace(',', '')
            processed_records.append((date, round(float(money), 4)))
        return processed_records

    def get_annual_roic(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, ROIC_TABLE)
        data = []
        for row in table_rows:
            date, _, _, roic = [td.text for td in row.find_all('td')]
            data.append((date, roic))

        data = self._process_precentage_records(data)
        return data

    def get_annual_revenue(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, REVENUE_TABLE)
        data = []
        for row in table_rows:
            date, revenue = [td.text for td in row.find_all('td')]
            data.append((date, revenue))

        data = self._process_dollar_records(data)
        return data

    def get_annual_cash(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, CASH_TABLE)
        data = []
        for row in table_rows:
            date, cash = [td.text for td in row.find_all('td')]
            data.append((date, cash))

        data = self._process_dollar_records(data)
        return data

    def get_annual_equity(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, EQUITY_TABLE)
        data = []
        for row in table_rows:
            date, cash = [td.text for td in row.find_all('td')]
            data.append((date, cash))

        data = self._process_dollar_records(data)
        return data

    def get_annual_eps(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, EPS_TABLE)
        data = []
        for row in table_rows:
            date, cash = [td.text for td in row.find_all('td')]
            data.append((date, cash))

        data = self._process_dollar_records(data)
        return data

    def get_ttm_pe(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, PE_TABLE)
        data = []
        for row in table_rows:
            date, _, _, pe = [td.text for td in row.find_all('td')]
            data.append((date, pe))

        data = self._process_dollar_records(data)
        return data

    def get_basic_shares_outstanding(self, url):
        soup = self._get_soup(url)
        table_rows = self._get_data_rows(soup, BASIC_SHARES_OUTSTANDING_TABLE)
        data = []
        for row in table_rows:
            date, bso = [td.text for td in row.find_all('td')]
            data.append((date, bso))

        data = self._process_dollar_records(data)
        return data

    def get_latest_value_from_top(self, soup, text_of_latest_line):
        line = soup.find_all(text=re.compile(text_of_latest_line))[0].parent
        value = line.find('strong').text
        value = value.replace('B', '')
        value = value.replace('$', '')
        return float(value) * 1000
