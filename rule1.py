from crawler import MacroTrendCrawler
from configs.url_config import *

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
        url = ROIC_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_roic(url)
        return data

    @property
    def equity(self):
        url = EQUITY_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_equity(url)
        return data

    @property
    def equity_growth(self):
        pass

    @property
    def eps(self):
        url = EPS_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_eps(url)
        return data

    @property
    def eps_growth(self):
        pass

    @property
    def revenue(self):
        url = REVENUE_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_revenue(url)
        return data

    @property
    def revenue_growth(self):
        pass

    @property
    def cash(self):
        url = CASH_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_cash(url)
        return data

    @property
    def cash_growth(self):
        pass

    def _compute_growth(self):
        pass

tool = RuleOne('chegg', 'CHGG')
print(f'roic: {tool.roic}')
print(f'revenue: {tool.revenue}')
print(f'cash: {tool.cash}')
print(f'equity: {tool.equity}')
print(f'eps: {tool.eps}')


# class MacroTrendCrawler:
#
#     def _get_soup(self, url):
#         r = requests.get(url)
#         r.raise_for_status()
#         html = r.text
#         soup = BeautifulSoup(html, 'html.parser')
#         return soup
#
#     def _get_data_rows(self, soup, table):
#         table = soup.find_all(text=re.compile(table))[0].parent.parent.parent.parent
#         table_rows = [ele for ele in table.find('tbody').find_all('tr')]
#         return table_rows
#
#     def _process_precentage_records(self, annual_records):
#         processed_records = []
#         for date, percentage in annual_records:
#             if percentage[:-1] == 'inf':
#                 break
#             processed_records.append((date, round(float(percentage[:-1]) * 0.01, 4)))
#         return processed_records
#
#     def _process_dollar_records(self, annual_records):
#         processed_records = []
#         for date, money in annual_records:
#             money = money[1:]
#             if not money:
#                 break
#             money = money.replace(',', '')
#             processed_records.append((date, round(float(money), 4)))
#         return processed_records
#
#     def get_annual_roic(self, url):
#         soup = self._get_soup(url)
#         table_rows = self._get_data_rows(soup, ROIC_TABLE)
#         data = []
#         for row in table_rows:
#             date, _, _, roic = [td.text for td in row.find_all('td')]
#             data.append((date, roic))
#
#         data = self._process_precentage_records(data)
#         return data
#
#     def get_annual_revenue(self, url):
#         soup = self._get_soup(url)
#         table_rows = self._get_data_rows(soup, REVENUE_TABLE)
#         data = []
#         for row in table_rows:
#             date, revenue = [td.text for td in row.find_all('td')]
#             data.append((date, revenue))
#
#         data = self._process_dollar_records(data)
#         return data
#
#     def get_annual_cash(self, url):
#         soup = self._get_soup(url)
#         table_rows = self._get_data_rows(soup, CASH_TABLE)
#         data = []
#         for row in table_rows:
#             date, cash = [td.text for td in row.find_all('td')]
#             data.append((date, cash))
#
#         data = self._process_dollar_records(data)
#         return data
#
#     def get_annual_equity(self, url):
#         soup = self._get_soup(url)
#         table_rows = self._get_data_rows(soup, EQUITY_TABLE)
#         data = []
#         for row in table_rows:
#             date, cash = [td.text for td in row.find_all('td')]
#             data.append((date, cash))
#
#         data = self._process_dollar_records(data)
#         return data
#
#     def get_annual_eps(self, url):
#         soup = self._get_soup(url)
#         table_rows = self._get_data_rows(soup, EPS_TABLE)
#         data = []
#         for row in table_rows:
#             date, cash = [td.text for td in row.find_all('td')]
#             data.append((date, cash))
#
#         data = self._process_dollar_records(data)
#         return data
#
# company_info = {'company': 'chegg',
#                 'ticker': 'CHGG'}
# scraper = MacroTrendCrawler()

