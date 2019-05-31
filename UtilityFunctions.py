'''

UtilityFunctions.py

File contents:
    functions
    ---------
        get_month_number
        get_nearest_expiry
        get_strike_n_below_price
        bull_cross
        bear_cross

'''


def bull_cross(p1, p0, m1, m0):
    '''Determines if line p crosses over from below to above line m'''
    if p0 <= m0:
        if p1 > m1:
            return True
    return False


def bear_cross(p1, p0, m1, m0):
    '''Determines if line p crosses over from above to below line m'''
    if p0 >= m0:
        if p1 < m1:
            return True
    return False


def get_month_number(df):
    '''Classifies dates by their month.'''
    base_year = df.index[0].year
    return [12 * (i.year - base_year) + i.month for i in df.index]


def get_nearest_expiry(time_a, min_days_to_expiry, expiry_series):
    '''Returns the closest expiration date after min_days.'''
    temp_df = (expiry_series - time_a).dt.days > min_days_to_expiry
    temp_df = expiry_series.loc[temp_df == True]
    if temp_df.shape[0] > 0:
        return temp_df.iloc[0]
    else:
        return None


def get_strike_n_below_price(S, n=1):
    '''Returns the closest strike after n strikes, assuming that strikes are multiples of 2.5'''
    return ((S // 2.5) - (n-1)) * 2.5