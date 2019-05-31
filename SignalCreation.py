'''

SignalCreation.py

File Contents:

    functions
    ---------
        call_buy_signal
        put_buy_signals
        expand_market_data

'''
import pandas as pd
from UtilityFunctions import bull_cross, bear_cross, get_month_number
from UtilityFunctions import  get_nearest_expiry, get_strike_n_below_price
from numpy import sqrt


# HELPER FUNCTIONS
# ================
def apply_signal(data, option_type):
    '''
    Applies the signal function of a specified option to the data

    inputs
    ------
        data - Market data as a pd.DataFrame with columns: [Price, MovingAverage]
        option_type - Either "call" or "put"

    return
    ------
        pd.DataFrame with columns: [Entry, Exit, In-trade]
    '''
    return {"call": call_signals, "put": put_signals}[option_type](data)


def create_entry_and_exit_signal(df, buy_signal_function, sell_signal_function):
    # This could be where some creative programming could exist to make the back test
    # be capable of doing advanced entry and exits. Could perhaps use a list of buy columns
    # and a list of sell columns that get used as input into the buy_signal_function
    # and sell_signal_function
    prev_df = df.shift()

    new_vals = {}
    for ind, row in df.iterrows():
        vec = [row.Price, prev_df.loc[ind].Price, row.MovingAverage, prev_df.loc[ind].MovingAverage]
        new_vals[ind] = [buy_signal_function(*vec), sell_signal_function(*vec)]

    return pd.DataFrame(new_vals, index=["Entry", "Exit"]).T


def determine_in_trade_state(df, temp_df, direction=1):
    '''Determines if the trade is currently "on"'''
    if direction > 0:
        temp_df["In_trade"] = df.Price > df.MovingAverage
    else:
        temp_df["In_trade"] = df.Price < df.MovingAverage

    # Add the end points if they are not already added
    temp_df["In_trade"] = temp_df.Entry | temp_df.Exit | temp_df.In_trade
    return temp_df


def calculate_optimal_strike(prices, option_type, n_strikes_away=1):
    '''Calculates the optimal strike assuming that strikes are all incremented $2.5 apart.'''
    strikes_below_price = n_strikes_away if option_type == "put" else -n_strikes_away
    return prices.apply(get_strike_n_below_price, n=strikes_below_price)


def calculate_optimal_expiration_date(time, exp_series, min_days_to_expiry=90):
    '''Determines the expiration date after the min_days_to_expiry value'''
    # return time.apply(get_nearest_expiry, min_days_to_expiry, exp_series)
    temp = []
    for ind, val in time.iteritems():
        temp.append(get_nearest_expiry(val, min_days_to_expiry, exp_series))

    return pd.Series(temp, index=time.index)


def calculate_historical_volatility(prices, volatility_window=10):
    return prices.pct_change().rolling(volatility_window).std() * sqrt(252)


def pad_data(df, moving_average_lag, volatility_window, min_days_to_expiry):
    '''
    Removes the NaN values from the beginning of the DataFrame as well as gives space for trades at the
    end to have room to trade and exit.
    '''
    start_up_window_length = max([moving_average_lag, volatility_window])
    frame_end_length = 2 * min_days_to_expiry
    return df.iloc[start_up_window_length:-frame_end_length]


# PUBLIC FUNCTIONS
# ================
def call_signals(df):
    '''Wrapper function to retrieve buy and sell signals for the call option'''
    temp_df = create_entry_and_exit_signal(df, bull_cross, bear_cross)
    return determine_in_trade_state(df, temp_df, 1)


def put_signals(df):
    '''Wrapper function to retrieve buy and sell signals for the put option'''
    temp_df = create_entry_and_exit_signal(df, bear_cross, bull_cross)
    return determine_in_trade_state(df, temp_df, -1)


def expand_market_data(price_series, option_type, moving_average_lag, exp_series):
    '''
    Expands an asset's price time series into its full data frame with signals and
    optimal option details.

    input
    -----
        price_series - pd.Series of asset prices
        moving_average_lag - parameter for the moving average lag
        option_type - either "put" or "call"

    returns
    -------
        market_data - pd.DataFrame of expanded data containing the following columns:
            * Price
            * MovingAverage
            * t - current time index
            * Month - current month number
            * Opt_T - optimal expiration date for the current day
            * Opt_K - optimal strike price for the current price
            * Volatility
            * Enter
            * Exit
            * In_trade
    '''
    market_data = price_series.to_frame()
    market_data.columns = ["Price"]
    market_data["MovingAverage"] = market_data.Price.rolling(moving_average_lag).mean()
    market_data["t"] = market_data.index.to_series()

    market_data["Month"] = get_month_number(market_data)

    min_days_to_expiry = 90
    market_data["Opt_T"] = calculate_optimal_expiration_date(market_data.t, exp_series, min_days_to_expiry)

    n_strikes_away = 1
    market_data["Opt_K"] = calculate_optimal_strike(market_data.Price, option_type, n_strikes_away)

    volatility_window = 20
    market_data["Volatility"] = calculate_historical_volatility(market_data.Price, volatility_window)

    option_signal = apply_signal(market_data, option_type)
    market_data = pd.concat([market_data, option_signal], axis=1)

    # Remove the NaN data from the Data Frame
    market_data = pad_data(market_data, moving_average_lag, volatility_window, min_days_to_expiry)

    return market_data
