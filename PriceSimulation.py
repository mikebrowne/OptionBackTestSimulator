'''

PriceSimulation.oy

File contents

    functions
    ---------
        ou_process_function
        simulate_expiry_date
        simulate_dates
        create_ou_process

'''

from numpy import random
from pandas import Series
import datetime as dt


def ou_process_function(S0, alpha, beta, sigma, sample_length):
    def ou(S, alpha, beta, sigma, dw):
        return -beta * (S - alpha) + sigma * dw

    dW = random.randn(sample_length - 1)
    prices = [S0]
    for i in range(sample_length - 1):
        S = prices[-1]
        prices.append(S + ou(S, alpha, beta, sigma, dW[i]))


    return prices


def simulate_expiry_dates(data):
    '''Simulates Expiration dates to be every 3rd Friday'''

    def is_third_friday(d):
        # https://stackoverflow.com/questions/18424467/python-third-friday-of-a-month
        return d.weekday() == 4 and 15 <= d.day <= 21

    return Series([day if is_third_friday(day) else None for day in data.index]).dropna()


def simulate_dates(data):
    def is_weekday(date):
        if date.weekday() == 5:
            return False
        elif date.weekday() == 6:
            return False
        return True

    num_trading_days = len(data)

    end_date = dt.date.today()

    dates = []

    current_date = end_date
    while len(dates) < num_trading_days:
        if is_weekday(current_date):
            dates.append(current_date)
        current_date = current_date - dt.timedelta(days=1)

    return dates[::-1]


def create_ou_process(S0=30, alpha=50, beta=0.01, sigma=0.5, sample_length=100, with_expiry=True):

    p = ou_process_function(S0, alpha, beta, sigma, sample_length)
    t = simulate_dates(p)
    S = Series(p, index=t)
    if with_expiry:
        return S, simulate_expiry_dates(S)
    else:
        return S
