'''

TradeLogic.py

File contents:
    functions
    ---------
        trade_size_logic
        trade_logic

'''

from BlackScholesOptionPricing import Option


def trade_size_logic(price, account_data, percent_cash=0.9):
    '''
    Determines the number of contracts to trade.

    input
    -----
        price - price of the asset
        account_data - Account object that tracks the cash and asset values
        percent_cash - percent of account to keep in cash

    returns
    -------
        num_contracts - the number of contracts to buy
    '''
    return int(((1 - percent_cash) * account_data.cash_value) // price)


def trade_logic(current_market_data, current_option, num_contracts, trade_size_logic, account_data, option_type):
    '''
    Basic trading logic for the strategy.

    inputs
    ------
        current_market_data - pd.DataFrame row with columns:
                                [Price, Opt_T, Opt_K, Volatility, Enter, Exit, In_trade]

        current_option - Option object fur the current option being traded

        num_contracts - Number of option contracts currently being held

        trade_size_logic - Function that determines the number of contracts to trade

        account_data - Account object that tracks the cash and asset values

        option_type - either "put" or "call"

    returns
    -------
        current_option, num_contracts
    '''
    cmd = current_market_data  # Short form to help make code fit

    if cmd.loc["In_trade"]:
        if cmd.loc["Entry"]:
            # Entering a position requires:
            #     1. Opening/selecting an option contract
            #     2. Getting the spot price of the option contract
            #     3. Determining the number of contracts to purchase
            #     4. Purchasing / adding the contracts to the portfolio
            #     5. Update stop loss data
            current_option = Option(cmd.loc["Opt_T"], cmd.loc["Opt_K"], option_type=option_type)
            option_price = current_option.price(cmd.loc["Price"], cmd.loc["Volatility"], cmd.loc["t"])
            num_contracts = trade_size_logic(option_price, account_data)
            account_data.enter_position(option_price, num_contracts)

        elif current_option is not None:
            # Since in the trade, will need to check and update the price of the option, requires:
            #     1. Getting the spot price of the option contract
            #     2. Updating the account details, which will depend on if the position is closing or not
            #     3. Update stop loss data
            option_price = current_option.price(cmd.loc["Price"], cmd.loc["Volatility"], cmd.loc["t"])

            if cmd.loc["Exit"]:
                # Reset current_option and num_contracts
                account_data.exit_position(option_price, num_contracts)
                current_option = None
                num_contracts = None

            else:
                # Simply add the updated information and continue
                account_data.update_position(option_price, num_contracts)

    return current_option, num_contracts
