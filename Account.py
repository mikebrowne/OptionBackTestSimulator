'''

Account.py

File contents:

    classes
    -------
        Account

'''


class Account:
    '''
        Holds the account data and provides functionality to adjust while trading.

        initial inputs
        --------------
        initial_cash - The amount of cash to start the back test with.

        attributes
        ----------
        asset_value - The current value of the assets held in the portfolio
        cash_value - The current value of the cash available in the portfolio

        methods
        -------
        enter_position - * Adjusts the cash and asset value of the account on entering a trade
                         * Inputs:
                             option_price, num_contracts

        update_position - * Adjusts the cash and asset value of the account while in a trade
                          * Inputs:
                              option_price, num_contracts

        exit_position - * Adjusts the cash and asset value of the account on exiting a trade
                        * Inputs:
                            option_price, num_contracts
        '''

    def __init__(self, initial_cash=50000):
        self.asset_value = None;
        self.cash_value = initial_cash

    @staticmethod
    def calculate_asset_value_(option_price, num_contracts):
        return option_price * num_contracts

    def enter_position(self, option_price, num_contracts):
        '''To enter a position, need to determine how many shares to purchase then adjust the balances'''
        current_asset_value = self.calculate_asset_value_(option_price, num_contracts)
        self.cash_value = self.cash_value - current_asset_value
        self.asset_value = current_asset_value

    def update_position(self, option_price, num_contracts):
        '''After the price has been updated, the asset value is adjusted.'''
        self.asset_value = self.calculate_asset_value_(option_price, num_contracts)

    def exit_position(self, option_price, num_contracts):
        '''To enter a position, need to sell all shares then adjust the balances'''
        current_asset_value = self.calculate_asset_value_(option_price, num_contracts)
        self.cash_value = self.cash_value + current_asset_value
        self.asset_value = None
