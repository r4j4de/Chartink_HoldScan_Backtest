# Equity Curve and Drawdown Analysis App
This Streamlit app analyzes equity returns and drawdown based on stock data provided in a CSV file or a backtested scan report from Chartink. It calculates cumulative returns, maximum cumulative returns, drawdown, and maximum drawdown percentage for each date in the dataset.

How to Use
Upload Backtested Scan Report from Chartink
Processing: The app will process each entry in the backtested scan report, fetching stock data for each date and symbol combination using yfinance Python library.

Display
Once processing is complete for either CSV file or backtested scan report, the app displays an interactive plot showing:

Cumulative Sum of Returns over time
Maximum Cumulative Sum of Returns
Drawdown (negative deviation from the maximum cumulative sum)
Maximum Drawdown with corresponding date
Date Formatting
The app automatically adjusts the date formatting on the x-axis based on the length of the dataset:

Installation - To run this app locally:

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the requirements

   ```
   pip install -r requirements.txt
   ```
   
3. Run the Streamlit app:
   
   ```
   streamlit run app.py
   ```
