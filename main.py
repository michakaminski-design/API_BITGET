import ccxt
import pandas as pd

# Inicjalizacja Bitget
exchange = ccxt.bitget()

def fetch_and_analyze(symbol, timeframe='1h', limit=50):
    # 1. Pobieranie danych
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # 2. Wykrywanie FVG
    fvg_data = []
    
    # Iteracja od 3. świecy (potrzebujemy min. 3 świec do FVG)
    for i in range(2, len(df)):
        prev_2 = df.iloc[i-2]
        current = df.iloc[i]
        
        # Bullish FVG: Low obecnej świecy > High świecy sprzed 2 okresów
        if current['low'] > prev_2['high']:
            fvg_data.append({
                'symbol': symbol,
                'interval': timeframe,
                'type': 'BULLISH',
                'fvg_start': prev_2['high'],
                'fvg_end': current['low'],
                'base_high': prev_2['high'],
                'base_low': prev_2['low']
            })
            
        # Bearish FVG: High obecnej świecy < Low świecy sprzed 2 okresów
        elif current['high'] < prev_2['low']:
            fvg_data.append({
                'symbol': symbol,
                'interval': timeframe,
                'type': 'BEARISH',
                'fvg_start': prev_2['low'],
                'fvg_end': current['high'],
                'base_high': prev_2['high'],
                'base_low': prev_2['low']
            })
            
    return fvg_data

# Przykładowe użycie:
# data = fetch_and_analyze('BTC/USDT', '1h')
# print(data[-1]) # Ostatnie wykryte FVG
