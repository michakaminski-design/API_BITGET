import ccxt
import pandas as pd
import gspread
import json
import os
import time
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. Konfiguracja ---
exchange = ccxt.bitget({'enableRateLimit': True})

LIMIT_MAP = {
    '1w': 5,
    '1d': 10,
    '4h': 15,
    '1h': 3,
    '15m': 3,
    '5m': 3
}

ASSET_GROUPS = {
    'TOP_LIQUIDITY': ['AAVE', 'ADA', 'ALGO', 'APE', 'ATOM', 'BCH', 'BNB', 'BTC', 'CHZ', 'CRV', 'DOGE', 'DOT', 'ETC', 'ETH', 'FIL', 'FLOW', 'GRT', 'ICP', 'INJ', 'LINK', 'LTC', 'MANA', 'NEAR', 'NEO', 'OP', 'POL', 'QNT', 'QTUM', 'RUNE', 'SHIB', 'SOL', 'SNX', 'TRX', 'TWT', 'UNI', 'XLM', 'XMR', 'XRP', 'XTZ', 'YFI', 'ZEC'],
    'MID_CAPS': ['1INCH', 'ACX', 'AGLD', 'AGX', 'ALCH', 'API3', 'APT', 'ARB', 'ARKM', 'ASTR', 'AUCTION', 'AXS', 'BICO', 'BIGTIME', 'BLUR', 'CAKE', 'CELO', 'CFX', 'COMP', 'DYDX', 'DYM', 'ENA', 'ENJ', 'ENS', 'GALA', 'GAS', 'GMX', 'HIGH', 'HBAR', 'IMX', 'IO', 'JASMY', 'JTO', 'JUP', 'KAVA', 'KNC', 'LDO', 'LRC', 'LPT', 'METIS', 'MINA', 'MOVR', 'MASK', 'MTL', 'NFP', 'NOT', 'ONDO', 'ORDI', 'PENDLE', 'PHB', 'POLYX', 'PYTH', 'REZ', 'RPL', 'RSR', 'RVN', 'SCR', 'SEI', 'STRK', 'STX', 'SUI', 'SUPER', 'TAO', 'THE', 'TIA', 'TON', 'TSTBSC', 'TURBO', 'UMA', 'VANRY', 'VIC', 'WLD', 'WOO', 'WIF', 'YGG', 'ZIL', 'ZRO'],
    'LOW_CAPS': ['1000LUNC', '4', 'ACT', 'AIXBT', 'AIX', 'AKE', 'ANIME', 'ANKR', 'APR', 'ARC', 'ARIA', 'ASTER', 'AT', 'B', 'B3', 'BAN', 'BARD', 'BLESS', 'BLUAI', 'BR', 'BROCCOLI', 'BTR', 'CARV', 'CC', 'CETUS', 'CKB', 'CLANKER', 'COW', 'CVC', 'DASH', 'DOOD', 'DOLO', 'DUSK', 'EDU', 'ENSO', 'ESPORTS', 'F', 'FLOCK', 'FLOKI', 'FLUID', 'GIGGLE', 'GRASS', 'GTC', 'GUN', 'H', 'HANA', 'HEI', 'HEMI', 'HIGH', 'HYPER', 'HYPE', 'ICNT', 'IP', 'INUSDT', 'JASMY', 'JCT', 'JELLYJELLY', 'JST', 'KAS', 'LAB', 'LIGHT', 'LINEA', 'LUMIA', 'LYN', 'M', 'MAGIC', 'MERL', 'MEW', 'MMT', 'MUBARAK', 'MYX', 'NAORIS', 'NEWT', 'NOM', 'OG', 'OGN', 'ONG', 'ONT', 'OPEN', 'ORBS', 'ORCA', 'PARTI', 'PAXG', 'PENGU', 'PEOPLE', 'PIPIN', 'PIEVERSE', 'PIXEL', 'PNUT', 'PTB', 'PUMP', 'Q', 'RAD', 'RARE', 'RED', 'RESOLV', 'RIVER', 'ROAM', 'SAGA', 'SAROS', 'SIGN', 'SKYAI', 'SOMI', 'STG', 'STO', 'SXT', 'TA', 'TNSR', 'TRUST', 'TRUTH', 'UA', 'USELESS', 'USUAL', 'USTC', 'VANA', 'VELVET', 'VINE', 'VIRTUAL', 'VVV', 'WAXP', 'WLFI', 'XNY', 'XPIN', 'XPLUS', 'XRO', 'ZBCN', 'ZBT', 'ZENT', 'ZEREBRO', 'ZKC', 'ZRX']
}

# --- 2. Logika Google Sheets ---
def get_gspread_client():
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def update_spreadsheet(fvg_data):
    if not fvg_data: return
    try:
        client = get_gspread_client()
        sheet = client.open('Twoj_Skaner_Wyniki').sheet1
        headers = ['category', 'symbol', 'interval', 'type', 'fvg_start', 'fvg_end', 'base_high', 'base_low']
        rows = [[d[h] for h in headers] for d in fvg_data]
        
        sheet.clear()
        sheet.append_row(headers)
        sheet.append_rows(rows)
        print(f"SUKCES: Zaktualizowano arkusz {len(rows)} rekordami.")
    except Exception as e:
        # Ignorujemy błędy typu [200], które są w rzeczywistości sukcesami
        if "200" in str(e):
            print("SUKCES: Dane zapisane (odpowiedź 200).")
        else:
            print(f"BŁĄD ZAPISU: {e}")

# --- 3. Logika Skanowania ---
def fetch_and_analyze(symbol, category, timeframe='1h'):
    try:
        pair = f"{symbol}/USDT"
        limit = LIMIT_MAP.get(timeframe.lower(), 50)
        ohlcv = exchange.fetch_ohlcv(pair, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        fvg_data = []
        i = len(df) - 1
        if i >= 2:
            prev_2 = df.iloc[i-2]
            current = df.iloc[i]
            
            if current['low'] > prev_2['high']:
                fvg_data.append({'category': category, 'symbol': pair, 'interval': timeframe, 'type': 'BULLISH', 'fvg_start': float(prev_2['high']), 'fvg_end': float(current['low']), 'base_high': float(prev_2['high']), 'base_low': float(prev_2['low'])})
            elif current['high'] < prev_2['low']:
                fvg_data.append({'category': category, 'symbol': pair, 'interval': timeframe, 'type': 'BEARISH', 'fvg_start': float(prev_2['low']), 'fvg_end': float(current['high']), 'base_high': float(prev_2['high']), 'base_low': float(prev_2['low'])})
        return fvg_data
    except Exception:
        return []

# --- 4. Główna pętla ---
if __name__ == "__main__":
    TIMEFRAME = '1h'
    all_results = []
    
    print("Rozpoczynam zoptymalizowane skanowanie...")
    for category, symbols in ASSET_GROUPS.items():
        for symbol in symbols:
            results = fetch_and_analyze(symbol, category, TIMEFRAME)
            if results:
                all_results.extend(results)
            time.sleep(0.05)

    if all_results:
        update_spreadsheet(all_results)
    else:
        print("Brak nowych sygnałów na ostatniej świecy.")
