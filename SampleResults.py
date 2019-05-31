from Backtest import Backtest
from PriceSimulation import create_ou_process
from TradeLogic import trade_size_logic

# Graphing
import matplotlib.pyplot as plt

ma_lag =100
option_type = "call"

price_series, expiration_series = create_ou_process(sample_length=2000) # with pre-set parameters

bt = Backtest(price_series, trade_size_logic, option_type, expiration_series, ma_lag)
bt.run_backtest()
results = bt.export_results_as_df()

fig, ax = plt.subplots(2, figsize=(12,7))
ax[0].set_title("Option Porfolio Value")
ax[1].set_title("Underlying Asset Value")
results.drop(["UnderlyingValue"], axis=1).plot(ax=ax[0])
results.AssetValue.rolling(15).mean().plot(ax=ax[0])
results.UnderlyingValue.plot(ax=ax[1])
results.UnderlyingValue.rolling(ma_lag).mean().plot(ax=ax[1])

plt.savefig("test_results.png")