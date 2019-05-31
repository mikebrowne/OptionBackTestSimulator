'''

BlackScholesOptionPricing.py

File contents:
    Classes
    -------
        Option

    Functions:
        call_option_prices
        put_option_prices

'''

from scipy.stats import norm
from numpy import sqrt, exp, log, power, max


def call_option_price(spot_price, strike, time_to_expiration, risk_free_rate, volatility):
    '''
    Calculates the Black-Scholes European call option prices.
    :param spot_price: The spot price of the underlying asset
    :param strike: The strike price for the option contract
    :param time_to_expiration: The time until expiration given as an annual percent
    :param risk_free_rate: The rate of a risk-free asset given as an annual percent
    :param volatility: The volatility of the underlying asset given as an annual percent
    :return: price of the option
    '''

    # Helper Functions
    def N(x):
        rv = norm()
        return rv.cdf(x)

    def d1(S, K, tau, r, vol):
        a = 1/(vol * sqrt(tau))
        b = log(S / K)
        c = r + power(vol, 2)/2
        return a * (b + c*tau)

    def d2(S, K, tau, r, vol):
        return d1(S, K, tau, r, vol) - vol * sqrt(tau)

    temp_vec = [spot_price, strike, time_to_expiration, risk_free_rate, volatility]

    # If the time to expiration is 0 then d1 will throw an error. It is known that the price of a call
    # option = max{S-K, 0}
    if time_to_expiration <= 0:
        return max([spot_price - strike, 0])

    present_value_strike = strike * exp(-risk_free_rate * time_to_expiration)
    return N(d1(*temp_vec)) * spot_price - N(d2(*temp_vec)) * present_value_strike


def put_option_price(spot_price, strike, time_to_expiration, risk_free_rate, volatility):
    '''
    Calculate the Black-Scholes European put option utilizing put-call paridy
    :param spot_price: The spot price of the underlying asset
    :param strike: The strike price for the option contract
    :param time_to_expiration: The time until expiration given as an annual percent
    :param risk_free_rate: The rate of a risk-free asset given as an annual percent
    :param volatility: The volatility of the underlying asset given as an annual percent
    :return: price of the option
    '''

    present_value_strike = strike * exp(-risk_free_rate * time_to_expiration)
    temp_vec = [spot_price, strike, time_to_expiration, risk_free_rate, volatility]
    return present_value_strike - spot_price + call_option_price(*temp_vec)


class Option:
    '''
    Option contract holder to keep track of which contract is currently held.

    initial inputs
    --------------
    T - Expiration Date
    K - Strike Price
    r - Risk-Free Rate (annualized)
    option_type - Type of the option (call or put)

    attributes
    ----------
    T - Expiration Date (annualized)
    K - Strike Price
    r - Risk-Free Rate (annualized)
    pricing_function - Option function type (Call or Put)

    methods
    -------
    price - * Uses the option pricing from above to calculate the option value.
            * Inputs:
                S - Spot price of the underlying asset
                Vol - The current volatility (annualized)
                t - Current time
    '''

    def __init__(self, T, K, r=0.03, option_type="call"):
        self.T = T; self.K = K; self.r = r;
        self.pricing_function = {"call": call_option_price, "put": put_option_price}[option_type]

    def format_tau(self, t):
        '''Annualized percent of time to expiration.'''
        return (self.T - t).days / 365

    def price(self, s, vol, t):
        tau = self.format_tau(t)
        return self.pricing_function(s, self.K, tau, self.r, vol)