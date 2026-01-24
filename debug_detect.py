#!/usr/bin/env python3

test_filenames = [
    "trades_20260120_215755.csv",
    "EURUSD_H1_trades_20260120.csv",
    "GBPUSD_M15_backtest.csv",
    "XAGEUR_D1_results.csv",
]

common_symbols = ['XAUUSD', 'XAGUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 
                'NZDUSD', 'USDCAD', 'USDCHF', 'EURGBP', 'EURJPY', 'GBPJPY',
                'XAGEUR', 'EURAUD', 'CADCHF', 'AUDNZD']

for filename in test_filenames:
    print(f"\nFile: {filename}")
    filename_base = filename.replace('.csv', '')
    parts = filename_base.split('_')
    print(f"  Parts: {parts}")
    
    symbol = "Unknown"
    for part in parts:
        print(f"    Checking: {part}")
        if part.upper() in common_symbols:
            symbol = part.upper()
            print(f"      -> Found symbol: {symbol}")
            break
    
    print(f"  Result: {symbol}")
