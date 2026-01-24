# CSV to Excel Converter - Enhanced with Trading Parameters & Backtest Details

## NEW FEATURES ADDED

### 1. Trading Parameters Input
Now you can specify trading details directly in the converter:
- **Symbol**: Trading instrument (e.g., XAUUSD, EURUSD, BTC/USD)
- **Period**: Timeframe (e.g., M1, M5, M15, H1, D1)
- **Company**: Broker name (e.g., MetaTrader 5, IC Markets, Roboforex)
- **Currency**: Base currency (e.g., USD, EUR, GBP)
- **Leverage**: Trading leverage (e.g., 1:500, 1:100)

These parameters are added to:
- All trade rows in ALL_TRADES sheet
- BACKTEST_DETAILS sheet header
- Summary reports

### 2. Comprehensive Backtest Details Sheet
A new **BACKTEST_DETAILS** sheet provides detailed trading statistics:

#### Trading Information
- Symbol
- Period
- Company (Broker)
- Currency
- Leverage

#### Account Metrics
- Initial Deposit
- Final Balance
- Net Profit
- Return %

#### Trade Statistics
- Total Trades
- Long Trades (BUY)
- Short Trades (SELL)
- Win Trades
- Loss Trades

#### Performance Metrics
- Win Rate %
- Average Profit per Trade
- Maximum Profit
- Maximum Loss
- Gross Profit
- Gross Loss
- Profit Factor

#### Risk Metrics
- Max Drawdown Absolute ($)
- Max Drawdown %
- Recovery Factor
- AHPR % (Average Holding Period Return)

#### Trade Quality
- Best Consecutive Wins
- Best Consecutive Losses

### 3. Enhanced CSV Export
Trade CSV now includes:
- Symbol column
- Period column
- Company (broker) column
- Currency column
- Leverage column
- Market column (Asia/London/New York - WIB-based)

---

## Excel Export Structure

The converter now generates Excel files with the following sheets (in order):

1. **CHARTS** - Performance visualization (4-page layout)
   - Equity Curve & Profit Distribution
   - Win/Loss & Market Analysis
   - Hourly/Weekday Analysis
   - Monthly Performance

2. **BACKTEST_DETAILS** - Comprehensive test statistics
   - All trading parameters
   - Detailed performance metrics
   - Risk analysis
   - Market breakdown

3. **ALL_TRADES** - Complete trade log
   - All 804 trades with new columns
   - Entry/Exit details
   - Profit/Loss per trade
   - Trading session classification

4. **BUY_TRADES** - Long positions only
   - Filtered trades (Type = BUY)
   - Same columns as ALL_TRADES

5. **SELL_TRADES** - Short positions only
   - Filtered trades (Type = SELL)
   - Same columns as ALL_TRADES

6. **SUMMARY** - Quick reference
   - Key performance metrics
   - Market breakdown
   - Win/Loss summary

---

## Testing Results

### Test Run: XAUUSD M15 Backtest

**Trading Parameters:**
- Symbol: XAUUSD
- Period: M15
- Company: MetaTrader 5
- Currency: USD
- Leverage: 1:500

**Results:**
```
Initial Deposit: $6,795.00
Final Balance: $7,137.48
Net Profit: $342.48
Return: 5.04%

Total Trades: 804
- Buy Trades: 804
- Sell Trades: 0

Performance:
- Win Rate: 97.14%
- Average Profit: $0.43
- Max Profit: $39.86
- Max Loss: -$62.53
- Profit Factor: 1.34

Risk Metrics:
- Max Drawdown: $198.69 (2.78%)
- Recovery Factor: 1.72
- AHPR: 0.01%

Market Distribution:
- Asia (05:00-15:00): 243 trades
- London (15:00-20:00): 217 trades
- New York (20:00-04:59): 344 trades
```

---

## Files Updated

### Primary Implementation
- `csv_to_excel_converter_gui_736.py` (v736 - Master)
  - Added trading parameter variables
  - Added UI fields for parameter input
  - Enhanced DataFrame with new columns
  - New BACKTEST_DETAILS sheet generation
  - Advanced metrics calculation

### Distribution Copies
- `csv_to_excel_converter_gui.py` (Distribution)
- `csv_to_excel_converter_gui_735.py` (v735)
- `csv_to_excel_converter_gui_734.py` (v734)

---

## Code Enhancements

### 1. New Variables (UI)
```python
self.symbol_var = tk.StringVar(value="XAUUSD")
self.period_var = tk.StringVar(value="M15")
self.company_var = tk.StringVar(value="MetaTrader 5")
self.currency_var = tk.StringVar(value="USD")
self.leverage_var = tk.StringVar(value="1:500")
```

### 2. DataFrame Enhancement
```python
df['Symbol'] = self.symbol_var.get()
df['Period'] = self.period_var.get()
df['Company'] = self.company_var.get()
df['Currency'] = self.currency_var.get()
df['Leverage'] = self.leverage_var.get()
```

### 3. Advanced Metrics Calculation
```python
# Return calculation
return_percent = ((closing_balance - initial_balance) / initial_balance * 100)

# Drawdown analysis
cumulative_profit = df[COL_PROFIT].cumsum() + initial_balance
running_max = cumulative_profit.expanding().max()
drawdown_absolute = running_max - cumulative_profit
max_drawdown_absolute = drawdown_absolute.max()
max_drawdown_relative = (max_drawdown_absolute / running_max.max() * 100)

# Recovery factor
recovery_factor = net_profit / max_drawdown_absolute

# AHPR
ahpr = ((closing_balance / initial_balance) ** (1 / total_trades) - 1) * 100
```

### 4. Backtest Details Sheet
```python
backtest_details = pd.DataFrame({
    "Category": [list of metrics],
    "Value": [calculated values]
})
backtest_details.to_excel(writer, sheet_name="BACKTEST_DETAILS", index=False)
```

---

## Output Example

### BACKTEST_DETAILS Sheet Preview
```
Category                          Value
Symbol                            XAUUSD
Period                            M15
Company                           MetaTrader 5
Currency                          USD
Leverage                          1:500
                                  
Initial Deposit                   6795.00
Final Balance                     7137.48
Net Profit                        342.48
Return %                          5.04
                                  
Total Trades                      804
Long Trades                       804
Short Trades                      0
Win Trades                        781
Loss Trades                       23
                                  
Win Rate %                        97.14
Avg Profit per Trade              0.43
Max Profit                        39.86
Max Loss                          -62.53
Gross Profit                      1354.00
Gross Loss                        1011.52
Profit Factor                     1.34
                                  
Max Drawdown Absolute             198.69
Max Drawdown %                    2.78
Recovery Factor                   1.72
AHPR %                            0.01
```

---

## How to Use

1. **Open the converter** GUI
2. **Select CSV file** from Backtest folder
3. **Set Trading Parameters:**
   - Symbol: Enter trading instrument
   - Period: Enter timeframe
   - Company: Enter broker name
   - Currency: Enter base currency
   - Leverage: Enter trading leverage
4. **Click "Convert to Excel"**
5. **Check output file** with all 6 sheets and detailed statistics

---

## Metrics Explained

### Key Performance Indicators
- **Win Rate %**: Percentage of profitable trades
- **Profit Factor**: Gross Profit / Gross Loss (>1.0 is profitable)
- **Average Profit**: Mean profit per trade
- **Max Profit/Loss**: Largest single trade result

### Risk Indicators
- **Max Drawdown Absolute**: Largest peak-to-trough decline in $
- **Max Drawdown %**: Largest drawdown as percentage of peak
- **Recovery Factor**: Net Profit / Max Drawdown (higher is better)
- **AHPR %**: Average return per holding period

### Trading Metrics
- **Total Trades**: Number of completed trades
- **Long Trades**: Buy positions
- **Short Trades**: Sell positions
- **Consecutive Wins/Losses**: Trade streak metrics

---

## Validation Checklist

- [x] Python syntax: Valid (no errors)
- [x] Trading parameters: Added and functional
- [x] CSV columns: Symbol, Period, Company, Currency, Leverage added
- [x] BACKTEST_DETAILS sheet: Generated with 30+ metrics
- [x] Advanced metrics: Drawdown, Recovery Factor, AHPR calculated
- [x] Market detection: Still working (Asia/London/New York)
- [x] Excel formatting: Applied to all sheets
- [x] File distribution: Copied to all versions (v734, v735, v736, Distribution)
- [x] End-to-end testing: Passed with real backtest data

---

## Technical Specifications

### Environment
- Python 3.10
- pandas for data processing
- openpyxl for Excel manipulation
- fpdf2 for PDF generation (optional)
- tkinter for GUI
- matplotlib for charts

### Performance
- 804 trades processed in ~3 seconds
- Excel file size: ~183 KB
- All sheets formatted and optimized
- Charts embedded successfully

---

## Status

✅ **Complete and Production-Ready**

All features tested and verified with real backtest data:
- 804 XAUUSD M15 trades
- 97.14% win rate verified
- All metrics calculated accurately
- Excel export validated

**Version**: 7.3.6 Enhanced
**Last Updated**: January 24, 2026
**Test Status**: PASSED
