'''

Backtest.py

File contents:

    Classes
    -------
        Backtest

'''


from Account import Account
from SignalCreation import expand_market_data
from TradeLogic import trade_logic
from pandas import DataFrame


class Backtest:
    '''
    attributes
    ----------
        market_data - Expanded market data of an underlying asset
        account_data - Account object to keep track of asset and cash value
        trade_size_logic - Function to determine the number of contracts to trade
        trade_journal - Dictionary object holding the asset, cash, and total value of the account
        expiry_series - Series of expiration dates

        current_option - The current option to be traded
        num_contracts - The current number of contracts of the option to be held

    methods
    -------
        run_backtest - runs the backtest
        update_trade_journal - function to update the trade_journal dictionary
        export_results_as_df - returns a pd.DataFrame object of the trade_journal
    '''

    def __init__(self, price_series, trade_size_logic, option_type, expiry_series, ma_lag=200):
        self.market_data = expand_market_data(price_series, option_type, ma_lag, expiry_series)
        self.account_data = Account()
        self.trade_size_logic = trade_size_logic
        self.trade_journal = {}
        self.option_type = option_type
        self.expiry_series = expiry_series

        self.current_option = None
        self.num_contracts = None

    def update_trade_journal(self, day):
        u_value = self.market_data.Price.loc[day]
        a_value = self.account_data.asset_value
        c_value = self.account_data.cash_value

        if a_value is None:
            p_value = c_value
        else:
            p_value = c_value + a_value

        self.trade_journal[day] = [u_value, a_value, c_value, p_value]

    def export_results_as_df(self):
        columns = ["UnderlyingValue", "AssetValue", "CashValue", "PortfolioValue"]
        return DataFrame(self.trade_journal, index=columns).T

    def run_backtest(self):
        for day, current_market_data in self.market_data.iterrows():
            input_vec = [current_market_data, self.current_option, self.num_contracts,
                         self.trade_size_logic, self.account_data, self.option_type]

            self.current_option, self.num_contracts = trade_logic(*input_vec)

            self.update_trade_journal(day)