import ccxt
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. Konfiguracja Google Sheets ---
def get_gspread_client():
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_json:
        raise ValueError("Brak zmiennej środowiskowej GOOGLE_CREDENTIALS! Ustaw ją w ustawieniach Render.")
    
    creds_dict = json.loads(creds_json)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def update_spreadsheet(fvg_data):
    if not fvg_data:
        print("Brak danych FVG do wysłania.")
        return

    try:
        client = get_gspread_client()
        # Nazwa arkusza musi się zgadzać z nazwą pliku na Twoim Dysku Google
        sheet = client.open('Twoj_Skaner_Wyniki').sheet1
        
        # Przygotowanie danych (konwersja listy słowników na listę list)
        headers = ['symbol', 'interval', 'type', 'fvg_start', 'fvg_end', 'base_high', 'base_low']
        rows = [[d[h] for h in headers] for d in fvg_data]
        
        # Czyszczenie i zapis
        sheet.clear()
        sheet.append_row(headers)
        sheet.append_rows(rows)
        
        # Jeśli kod dotarł tutaj, zapis przebiegł pomyślnie
        print(f"SUKCES: Pomyślnie wysłano {len(rows)} wierszy do arkusza.")
        
    except Exception as e:
        # Ten blok wykona się tylko w razie faktycznego błędu połączenia lub uprawnień
        print(f"BŁĄD KRYTYCZNY podczas zapisu do arkusza: {e}")

# --- 2. Logika Skanowania (Bitget) ---
exchange = ccxt.bitget()

def fetch_and_analyze(symbol, timeframe='1h', limit=50):
    # 1. Pobieranie danych
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Błąd pobierania danych z giełdy: {e}")
        return []
    
    # 2. Wykrywanie FVG
    fvg_data = []
    
    # Iteracja od 3. świecy
    for i in range(2, len(df)):
        prev_2 = df.iloc[i-2]
        current = df.iloc[i]
        
        # Bullish FVG: Low obecnej świecy > High świecy sprzed 2 okresów
        if current['low'] > prev_2['high']:
            fvg_data.append({
                'symbol': symbol,
                'interval': timeframe,
                'type': 'BULLISH',
                'fvg_start': float(prev_2['high']),
                'fvg_end': float(current['low']),
                'base_high': float(prev_2['high']),
                'base_low': float(prev_2['low'])
            })
            
        # Bearish FVG: High obecnej świecy < Low świecy sprzed 2 okresów
        elif current['high'] < prev_2['low']:
            fvg_data.append({
                'symbol': symbol,
                'interval': timeframe,
                'type': 'BEARISH',
                'fvg_start': float(prev_2['low']),
                'fvg_end': float(current['high']),
                'base_high': float(prev_2['high']),
                'base_low': float(prev_2['low'])
            })
            
    return fvg_data

# --- 3. Główna pętla programu ---
if __name__ == "__main__":
    SYMBOL = 'BTC/USDT'
    TIMEFRAME = '1h'
    
    print(f"Rozpoczynam analizę dla {SYMBOL}...")
    results = fetch_and_analyze(SYMBOL, TIMEFRAME)
    
    if results:
        print(f"Znaleziono {len(results)} FVG. Wysyłam do arkusza...")
        update_spreadsheet(results)
    else:
        print("Nie znaleziono żadnych FVG lub wystąpił błąd pobierania.")
