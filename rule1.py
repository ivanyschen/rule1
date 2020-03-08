import numpy as np

from crawler import MacroTrendCrawler
from configs.url_config import *

class RuleOne:

    def __init__(self, company=None, ticker=None):
        self._company = company.lower().replace(' ', '-')
        self._ticker = ticker.upper()
        self._basic_shares_outstanding = None

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

    def roic(self):
        url = ROIC_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_roic(url)
        return data

    def equity(self, per_share=False):
        url = EQUITY_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_equity(url)
        data = [(date, equ) for date, equ in data if equ != 0]

        if per_share:
            return self._compute_per_share_value(data[:], self.basic_shares_outstanding[:])
        return data

    def equity_growth(self):
        return self._compute_growth(self.equity())

    def eps(self):
        url = EPS_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_eps(url)
        return data

    def eps_growth(self):
        return self._compute_growth(self.eps())

    def revenue(self, per_share=False):
        url = REVENUE_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_revenue(url)

        if per_share:
            return self._compute_per_share_value(data[:], self.basic_shares_outstanding[:])
        return data

    def revenue_growth(self):
        return self._compute_growth(self.revenue())

    def cash(self, per_share=False):
        url = CASH_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_annual_cash(url)

        if per_share:
            return self._compute_per_share_value(data[:], self.basic_shares_outstanding[:])
        return data

    def cash_growth(self):
        return self._compute_growth(self.cash())

    def pe_ratio(self):
        url = PE_URL.format(ticker=self._ticker, company=self._company)
        data = MacroTrendCrawler().get_ttm_pe(url)
        return data

    def pe_stats(self):
        data = [pe for _, pe in self.pe_ratio()[:20]]
        max_ = np.max(data)
        min_ = np.min(data)
        mean = np.mean(data)
        median = np.median(data)
        variance = np.var(data)
        return max_, min_, mean, median, variance

    @property
    def basic_shares_outstanding(self):
        if self._basic_shares_outstanding is None:
            url = BASIC_SHARES_OUTSTANDING_URL.format(ticker=self._ticker, company=self._company)
            data = MacroTrendCrawler().get_basic_shares_outstanding(url)
            self._basic_shares_outstanding = data
        return self._basic_shares_outstanding

    def print_rule_one_report(self, per_share=False):
        print(f'ROIC: {tool.roic()}')
        if per_share:
            print(f'equity (per share): {tool.equity(per_share)}')
        else:
            print(f'equity: {tool.equity(per_share)}')
        print(f'equity growth: {tool.equity_growth()}')
        print(f'eps: {tool.eps()}')
        print(f'eqs growth: {tool.eps_growth()}')
        if per_share:
            print(f'revenue (per share): {tool.revenue(per_share)}')
        else:
            print(f'revenue: {tool.revenue(per_share)}')
        print(f'revenue growth: {tool.revenue_growth()}')
        if per_share:
            print(f'cash ([er share): {tool.cash(per_share)}')
        else:
            print(f'cash: {tool.cash(per_share)}')
        print(f'cash growth: {tool.cash_growth()}')
        print(f'historical PE: {tool.pe_ratio()}')
        print('PE stats:\n'
              '\tmax: {}\n'
              '\tmin: {}\n'
              '\tmean: {}\n'
              '\tmedian: {}\n'
              '\tvariance: {}\n'.format(*tool.pe_stats()))

    def _compute_growth(self, data):
        growth_rates = []
        years_to_compute = (1, 5, 10, 15)
        _, cur_num = data[0]
        for i, (_, num) in enumerate(data):
            if i not in years_to_compute:
                continue
            try:
                growth_rate = (cur_num / num) ** (1 / i) - 1
                growth_rates.append((i, growth_rate))
            except ZeroDivisionError:
                growth_rates.append((i, 0))
        if i not in years_to_compute:
            try:
                growth_rate = (cur_num / data[i][1]) ** (1 / i) - 1
                growth_rates.append((i, growth_rate))
            except ZeroDivisionError:
                growth_rates.append((i, 0))

        return growth_rates

    def _compute_per_share_value(self, values, shares):
        if values[0][0] < shares[0][0]:
            shares = shares[1:]
        elif shares[0][0] < values[0][0]:
            values = values[1:]

        per_share_value = []
        for value, share in zip(values, shares):
            year = value[0]
            per_share_value.append((year, round(value[1] / share[1], 2)))

        return per_share_value

tool = RuleOne('ross store', 'rost')
tool.print_rule_one_report(True)
