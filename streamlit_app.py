import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm

holding_days = 10

def returns_stock(symbol, start_date, holding_days, entry="Close", exit="Close"):
    dt = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=holding_days*2)
    end_date = dt.strftime('%Y-%m-%d')
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    return_days = (stock_data[exit].iloc[int(holding_days)] - stock_data[entry].iloc[0]) / stock_data[entry].iloc[0]
    return return_days * 100

def main():
    st.title('Equity Curve and Drawdown Analysis')

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        returns_dict = {}
        for n in tqdm(range(len(df)), desc="Processing"):
            try:
                date = df.iloc[n, 0]
                date_obj = datetime.strptime(date, '%d-%m-%Y')
                date = date_obj.strftime('%Y-%m-%d')
                script = f"{df.iloc[n, 1]}.NS"
                if date in returns_dict:
                    signal_return = returns_stock(script, date, holding_days=holding_days, entry="Close", exit="Close")
                    returns_dict[date].append(signal_return)
                else:
                    signal_return = returns_stock(script, date, holding_days=holding_days, entry="Close", exit="Close")
                    returns_dict[date] = [signal_return]
            except:
                pass

        for date in returns_dict:
            returns = returns_dict[date]
            avg_return = (sum(returns) / len(returns)) / holding_days
            returns_dict[date] = avg_return

        returns_list = list(returns_dict.values())
        cumulative_sum = np.cumsum(returns_list)
        max_cumulative_sum = np.maximum.accumulate(cumulative_sum)
        drawdown = -1 * (max_cumulative_sum - cumulative_sum)
        max_drawdown = np.min(drawdown)
        max_drawdown_index = np.argmin(drawdown)

        dates = list(returns_dict.keys())
        date_format = '%Y-%m-%d'
        dates = [pd.to_datetime(date, format=date_format) for date in dates]

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(dates, cumulative_sum, label='Cumulative Sum')
        ax.plot(dates, max_cumulative_sum, label='Max Cumulative Sum')
        ax.fill_between(dates, cumulative_sum, max_cumulative_sum, facecolor='red', alpha=0.3)
        ax.plot(dates, drawdown, label='Drawdown')
        ax.axhline(y=max_drawdown, linestyle='--', color='k', label=f'Max Drawdown: {round(max_drawdown)}%')
        ax.axvline(x=dates[max_drawdown_index], linestyle='--', color='k')
        ax.axhline(y=0, linestyle='--', color='r')

        if len(dates) <= 90:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        elif len(dates) <= 700:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        else:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

        plt.xticks(rotation=45)
        ax.legend()

        st.pyplot(fig)

if __name__ == '__main__':
    main()
